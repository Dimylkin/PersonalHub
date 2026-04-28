from enum import StrEnum
from typing import Any


class OpenAPITags(StrEnum):
    BOARD = "Таблица"
    COLUMN = "Колонка"
    TASK = "Задача"

    @classmethod
    def get_openapi_tags(cls) -> list[dict[str, Any]]:
        return [
            {"name": cls.BOARD},
            {"name": cls.COLUMN},
            {"name": cls.TASK},
        ]
