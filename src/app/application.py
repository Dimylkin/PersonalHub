from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.lifespan import lifespan
from app.logger.config import setup_logger
from interfaces.routes import router


def get_app() -> FastAPI:
    """Получить FastAPI приложение.

    Это главный конструктов приложения.

    Returns:
        FastAPI приложение
    """
    setup_logger()

    app = FastAPI(
        title="PersonalHub-API",
        version="0.1.0",
        description="API сервиса PersonalHub",
        default_response_class=JSONResponse,
        lifespan=lifespan,
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        redoc_url="/api/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router, prefix="/api")

    # Инициализация JSON-обработчиков ошибок
    # Порядок важен: более специфичные обработчики должны быть зарегистрированы первыми

    # Prometheus FastAPI Instrumentator
    instrumentator = Instrumentator(
        should_group_status_codes=True,  # группировать коды ответов 2xx, 4xx, 5xx
        should_ignore_untemplated=True,  # игнорировать пути без шаблонов
        should_respect_env_var=False,  # не читать настройки из env
    )
    instrumentator.instrument(app)
    instrumentator.expose(
        app,
        include_in_schema=False,
        endpoint="/api/metrics",
    )

    return app
