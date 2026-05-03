from typing import Any

from fastapi import HTTPException
from starlette import status

from exceptions.base.enum import ModuleEnum
from exceptions.base.response import ErrorResponse


class AppError(Exception):
    code: str = "UNEXPECTED_ERROR"
    module: ModuleEnum = ModuleEnum.core
    http_status: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message: str | None = None

    def __init__(
        self,
        *,
        message: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.message = message or self.default_message or self.code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "module": self.module,
            "message": self.message,
            "details": self.details,
        }

    def json(self) -> dict[str, Any]:
        return self.to_dict()

    def to_http(self) -> HTTPException:
        return HTTPException(
            status_code=self.http_status,
            detail=self.to_dict(),
        )

    def to_response(self) -> ErrorResponse:
        return ErrorResponse(
            code=self.code,
            module=self.module,
            message=self.message,
            details=self.details,
        )

    def __str__(self) -> str:
        return str(self.to_dict())
