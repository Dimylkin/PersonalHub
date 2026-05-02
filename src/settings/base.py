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
    

class DBSettings(BaseSettings):
    model_config = BASE_MODEL_CONFIG

    HOST: str = Field(..., validation_alias="DB_HOST")
    PORT: int = Field(..., validation_alias="DB_PORT")
    USER: str = Field(..., validation_alias="DB_USER")
    PASSWORD: str = Field(..., validation_alias="DB_PASSWORD")
    NAME: str = Field(..., validation_alias="DB_NAME")
    ECHO: bool = Field(..., validation_alias="DB_ECHO")

    DRIVER: str = Field(default="postgresql+asyncpg")

    @property
    def URL(self) -> str:
        return (
            f"{self.DRIVER}://"
            f"{self.USER}:{self.PASSWORD}@"
            f"{self.HOST}:{self.PORT}/"
            f"{self.NAME}"
        )


class Settings:
    APP: AppSettings
    DB: DBSettings

    def __init__(self) -> None:
        self.APP = AppSettings()
        self.DB = DBSettings() # type: ignore[call-arg]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
