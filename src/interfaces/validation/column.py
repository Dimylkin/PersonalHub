from typing import Annotated
from datetime import datetime as dt

from pydantic import BaseModel, Field

from entities.enums import TypeColumn
from interfaces.dependencies.identifier import BoardID, ColumnID, Order


EXAMPLES_TYPE_COLUMN = [e.value for e in TypeColumn]


class ColumnCreateRequest(BaseModel):
    """Запрос на создание колонки."""

    board_id: Annotated[
        BoardID,
        Field(
            description="ID доски, к которой относится колонка",
            examples=[123],
        ),
    ]

    type: Annotated[
        TypeColumn,
        Field(
            description="Тип колонки",
            examples=EXAMPLES_TYPE_COLUMN,
        ),
    ]

    order: Annotated[
        Order,
        Field(
            description="Позиция колонки на доске",
            examples=[123],
        ),
    ]


class ColumnUpdateRequest(BaseModel):
    """Запрос на обновление колонки."""

    board_id: Annotated[
        BoardID | None,
        Field(
            description="ID доски (опционально)",
            examples=[123],
        ),
    ] = None

    type: Annotated[
        TypeColumn | None,
        Field(
            description="Тип колонки (опционально)",
            examples=EXAMPLES_TYPE_COLUMN,
        ),
    ] = None

    order: Annotated[
        Order | None,
        Field(
            description="Позиция колонки (опционально)",
            examples=[123],
        ),
    ] = None


class ColumnResponse(BaseModel):
    """Ответ с данными колонки."""

    id: Annotated[
        ColumnID,
        Field(
            description="Уникальный идентификатор колонки",
            examples=[123],
        ),
    ]

    board_id: Annotated[
        BoardID,
        Field(
            description="ID доски",
            examples=[123],
        ),
    ]

    type: Annotated[
        TypeColumn,
        Field(
            description="Тип колонки",
            examples=EXAMPLES_TYPE_COLUMN,
        ),
    ]

    order: Annotated[
        Order,
        Field(
            description="Позиция колонки",
            examples=[123],
        ),
    ]

    created_at: Annotated[
        dt,
        Field(
            description="Дата создания (UTC)",
            examples=["2026-05-03T14:00:00Z"],
        ),
    ]

    updated_at: Annotated[
        dt | None,
        Field(
            description="Дата обновления (UTC)",
            examples=["2026-05-03T15:00:00Z"],
        ),
    ]

    model_config = {
        "from_attributes": True,
    }
