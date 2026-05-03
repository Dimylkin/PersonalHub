from typing import Any

from fastapi import status

from exceptions.base.error import AppError

class NotFoundObjectException(AppError):
    code = "OBJECT_NOT_FOUND"
    http_status = status.HTTP_404_NOT_FOUND

    def __init__(
        self,
        object_name: str,
        object_id: int | str | None = None,
        details: dict[str, Any] | None = None,
    ):
        if object_id is not None:
            super().__init__(
                message=f"Объект {object_name} с id: {object_id} не найден",
                details=details or {"id": object_id},
            )
        else:
            super().__init__(message=f"Объект {object_name} не найден", details=details)