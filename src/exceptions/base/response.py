from typing import Any

from pydantic import BaseModel, Field

from exceptions.base.enum import ModuleEnum


class ErrorResponse(BaseModel):
    code: str = Field(..., description="Код ошибки")
    module: ModuleEnum = Field(..., description="Модуль, в котором произошла ошибка")
    message: str = Field(..., description="Сообщение ошибки")
    details: dict[str, Any] | None = Field(default_factory=dict, description="Детали ошибки")
