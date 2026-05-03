from typing import Any

from exceptions.base.error import AppError
from exceptions.base.response import ErrorResponse

BASE_ERROR_RESPONSES = {
    400: {"model": ErrorResponse, "description": "Ошибка запроса"},
    401: {"model": ErrorResponse, "description": "Нет авторизации"},
    403: {"model": ErrorResponse, "description": "Доступ запрещен"},
    404: {"model": ErrorResponse, "description": "Не найдено"},
    422: {"model": ErrorResponse, "description": "Ошибка валидации"},
    500: {"model": ErrorResponse, "description": "Внутренняя ошибка сервера"},
}

_STATUS_DESCRIPTIONS = {
    400: "Ошибка запроса",
    401: "Нет авторизации",
    403: "Доступ запрещён",
    404: "Не найдено",
    409: "Конфликт",
    413: "Payload слишком большой",
    415: "Неподдерживаемый тип медиа",
    422: "Ошибка валидации",
    500: "Внутренняя ошибка сервера",
}


def api_response(
    description: str,
    status_code: int = 200,
    errors: list[type[AppError]] | None = None,
) -> dict[int | str, dict[str, Any]]:
    """Формирует словарь responses для FastAPI-эндпоинта.

    Args:
        description: описание успешного ответа.
        status_code: HTTP-код успешного ответа (по умолчанию 200).
        errors: список классов AppError, которые может выбросить эндпоинт.
            Для каждого класса генерируется пример в документации Swagger.
    """
    result: dict[int | str, dict[str, Any]] = {
        status_code: {"description": description},
        **BASE_ERROR_RESPONSES,  # type: ignore[dict-item]
    }

    if not errors:
        return result

    by_status: dict[int, list[type[AppError]]] = {}
    for err_cls in errors:
        by_status.setdefault(err_cls.http_status, []).append(err_cls)

    # Статус-коды без тела ответа (RFC 7230)
    _no_body_statuses = {201, 204, 304}

    for http_status, err_classes in by_status.items():
        if http_status in _no_body_statuses:
            result[http_status] = {
                "description": _STATUS_DESCRIPTIONS.get(http_status, str(http_status)),
            }
            continue
        examples = {
            err_cls.code: {
                "summary": err_cls.default_message or err_cls.code,
                "value": {
                    "code": err_cls.code,
                    "module": err_cls.module,
                    "message": err_cls.default_message or err_cls.code,
                    "details": {},
                },
            }
            for err_cls in err_classes
        }
        result[http_status] = {
            "model": ErrorResponse,
            "description": _STATUS_DESCRIPTIONS.get(http_status, "Ошибка"),
            "content": {"application/json": {"examples": examples}},
        }

    return result
