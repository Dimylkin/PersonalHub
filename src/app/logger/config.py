import json
import logging
import logging.config
import sys
import traceback as tb_module
from typing import Any, cast

import structlog


def setup_logger() -> None:
    """Настраивает логирование в зависимости от STAGE."""
    # Настраиваем стандартный logging (для uvicorn и других библиотек)
    logging.config.dictConfig(get_logging_config())

    structlog.configure(
        processors=[
            # объединение контекста
            structlog.contextvars.merge_contextvars,
            # добавит logger name, level
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            # time в ISO
            structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),
            # если logger.exception(...) — положит exception как поле
            structlog.processors.format_exc_info,
            # line/file/function
            structlog.processors.CallsiteParameterAdder(
                parameters={
                    structlog.processors.CallsiteParameter.FILENAME,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                    structlog.processors.CallsiteParameter.LINENO,
                },
            ),
            # финальный процессор: dev или prod
            _dev_processor
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


class JSONFormatter(logging.Formatter):
    """
    JSON форматтер для библиотек, использующих стандартный logging.

    Преобразует логи в простой JSON формат.
    """

    def format(self, record: logging.LogRecord) -> str:
        log_data: dict[str, Any] = {
            "message": record.getMessage(),
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S.%03dZ"),
            "level": record.levelname,
            "logger": record.name,
        }
        return json.dumps(log_data, ensure_ascii=False)


class PlainTextHandler(logging.StreamHandler[Any]):
    """
    Handler для structlog.

    Выводит сообщение как есть, без добавления traceback.
    """

    def format(self, record: logging.LogRecord) -> str:
        return record.getMessage()


def get_logging_config() -> dict[str, Any]:
    """Возвращает конфигурацию logging для uvicorn и других библиотек."""
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            # JSON форматтер для библиотек (httpx, httpcore)
            "json": {"()": "app.logger.config.JSONFormatter"},
        },
        "handlers": {
            # Handler для structlog — без форматирования (он сам форматирует в JSON)
            "structlog_handler": {
                "()": "app.logger.config.PlainTextHandler",
                "stream": "ext://sys.stdout",
            },
            # Handler для httpx/httpcore — с JSON форматтером
            "json_handler": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "json",
            },
        },
        "loggers": {
            # Отключаем uvicorn логи — они дублируют lifespan logger
            "uvicorn": {"handlers": [], "level": "CRITICAL", "propagate": False},
            "uvicorn.error": {"handlers": [], "level": "CRITICAL", "propagate": False},
            "uvicorn.access": {"handlers": [], "level": "CRITICAL", "propagate": False},
            # HTTP клиентские логи (httpx/httpcore) — в JSON формате
            "httpx": {"handlers": ["json_handler"], "level": "INFO", "propagate": False},
            "httpcore": {"handlers": ["json_handler"], "level": "INFO", "propagate": False},
        },
        "root": {"handlers": ["structlog_handler"], "level": "INFO", "propagate": False},
    }


def _dev_processor(
    logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> str:
    """
    Процессор для dev-режима: выводит traceback в консоль, затем возвращает JSON.
    """
    exc_info = event_dict.pop("exc_info", None)
    exception_str = event_dict.pop("exception", None)  # format_exc_info добавляет это поле

    # Если есть exception, выводим traceback отдельно
    if exc_info or exception_str:
        if exc_info is True:
            exc_type, exc_value, exc_traceback = sys.exc_info()
        elif isinstance(exc_info, tuple) and len(exc_info) == 3:
            exc_type, exc_value, exc_traceback = exc_info
        else:
            exc_type, exc_value, exc_traceback = sys.exc_info()

        if exc_type and exc_value and exc_traceback:
            print("\n" + "=" * 80, file=sys.stderr)
            print("TRACEBACK (dev mode):", file=sys.stderr)
            print("=" * 80, file=sys.stderr)
            tb_lines = tb_module.format_exception(exc_type, exc_value, exc_traceback)
            for line in tb_lines:
                print(line, end="", file=sys.stderr)
            print("=" * 80, file=sys.stderr)
            print(file=sys.stderr)

    # Формируем JSON (без exception поля)
    json_renderer = structlog.processors.JSONRenderer(ensure_ascii=False)
    return cast(str, json_renderer(logger, method_name, event_dict))


def _prod_processor(
    logger: Any,
    method_name: str,
    event_dict: structlog.types.EventDict,
) -> str:
    """
    Процессор для prod-режима: добавляет traceback в JSON.
    """
    exc_info = event_dict.pop("exc_info", None)
    exception_str = event_dict.pop("exception", None)  # format_exc_info добавляет это поле

    if exc_info or exception_str:
        if exc_info is True:
            exc_type, exc_value, exc_traceback = sys.exc_info()
        elif isinstance(exc_info, tuple) and len(exc_info) == 3:
            exc_type, exc_value, exc_traceback = exc_info
        else:
            # Пытаемся получить из sys.exc_info() если exception_str есть
            exc_type, exc_value, exc_traceback = sys.exc_info()

        if exc_type and exc_value and exc_traceback:
            tb_lines = tb_module.format_exception(exc_type, exc_value, exc_traceback)
            traceback_str = "".join(tb_lines).replace("\n", "\\n")
            event_dict["traceback"] = traceback_str

    # Удаляем exc_info и exception чтобы logging не выводил traceback отдельно
    event_dict.pop("exc_info", None)
    event_dict.pop("exception", None)

    # Формируем JSON
    json_renderer = structlog.processors.JSONRenderer(ensure_ascii=False)
    return cast(str, json_renderer(logger, method_name, event_dict))
