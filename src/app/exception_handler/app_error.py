import structlog
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from exceptions.base.error import AppError

logger = structlog.stdlib.get_logger(__name__)


def init_json_for_app_error(
    app_: FastAPI,
    use_logger: bool = True,
) -> None:
    """Инициализация слушателя для AppError."""

    @app_.exception_handler(AppError)
    async def custom_http_exception_handler(
        request: Request,
        exc: AppError,
    ) -> JSONResponse:
        if use_logger and exc.http_status >= 500:
            ctx = getattr(request.state, "log_context", {})
            logger.bind(**ctx).exception(exc.message, exc_info=exc)

        return JSONResponse(
            status_code=exc.http_status,
            content=exc.to_dict(),
        )
