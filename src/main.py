from uvicorn import run

from app.logger.config import get_logging_config
from settings.base import get_settings

def main() -> None:
    settings = get_settings()

    run(
        "app.application:get_app",
        host=settings.APP.HOST,
        port=settings.APP.PORT,
        access_log=True,
        log_config=get_logging_config(),
        forwarded_allow_ips="*",
        factory=True,
        log_level="debug",
        reload=True,
    )


if __name__ == "__main__":
    main()
