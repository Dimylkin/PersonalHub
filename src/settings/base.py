from typing import Any

from anyio.functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings
from settings.config import BASE_MODEL_CONFIG

class AppSettings(BaseSettings):
    model_config = BASE_MODEL_CONFIG

    NAME: str = Field(..., validation_alias="APP_NAME")
    HOST: str = Field(...)
    PORT: int = Field(..., validation_alias="APP_PORT")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    @property
    def server_url(self) -> str:
        return f"http://{self.HOST}:{self.PORT}"


class Settings:
    APP: AppSettings

    def __init__(self) -> None:
        self.APP = AppSettings()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
