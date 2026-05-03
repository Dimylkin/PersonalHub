from datetime import datetime as dt
from typing import Annotated

from pydantic import BaseModel, Field, NonNegativeInt

from entities.enums import UrgencyTask
from interfaces.dependencies.identifier import ColumnID, Order, TaskID, BoardID


EXAMPLES_URGENCY = [e.value for e in UrgencyTask]


class TaskCreateRequest(BaseModel):
    """Запрос на создание задачи."""

    column_id: Annotated[
        ColumnID,
        Field(description="ID колонки", examples=[123]),
    ]

    title: Annotated[
        str,
        Field(description="Название задачи", examples=["abc"]),
    ]

    description: Annotated[
        str | None,
        Field(description="Описание задачи", examples=["abc"]),
    ] = None

    urgency: Annotated[
        UrgencyTask,
        Field(description="Приоритет задачи", examples=EXAMPLES_URGENCY),
    ]

    order: Annotated[
        Order,
        Field(description="Позиция задачи в колонке", examples=[123]),
    ]

    start_at: Annotated[
        dt | None,
        Field(description="Дата начала (UTC)", examples=["2026-05-03T14:00:00Z"]),
    ] = None

    end_at: Annotated[
        dt | None,
        Field(description="Дата окончания (UTC)", examples=["2026-05-03T15:00:00Z"]),
    ] = None


class TaskUpdateRequest(BaseModel):
    """Запрос на обновление задачи."""

    column_id: Annotated[
        ColumnID | None,
        Field(description="ID колонки", examples=[123]),
    ] = None

    title: Annotated[
        str | None,
        Field(description="Название задачи", examples=["abc"]),
    ] = None

    description: Annotated[
        str | None,
        Field(description="Описание задачи", examples=["abc"]),
    ] = None

    urgency: Annotated[
        UrgencyTask | None,
        Field(description="Приоритет задачи", examples=EXAMPLES_URGENCY),
    ] = None

    order: Annotated[
        Order | None,
        Field(description="Позиция задачи", examples=[123]),
    ] = None

    start_at: Annotated[
        dt | None,
        Field(description="Дата начала (UTC)", examples=["2026-05-03T14:00:00Z"]),
    ] = None

    end_at: Annotated[
        dt | None,
        Field(description="Дата окончания (UTC)", examples=["2026-05-03T15:00:00Z"]),
    ] = None


class TaskResponse(BaseModel):
    """Ответ с данными задачи."""

    id: Annotated[
        TaskID,
        Field(description="Уникальный ID задачи", examples=[123]),
    ]

    column_id: Annotated[
        ColumnID,
        Field(description="ID колонки", examples=[123]),
    ]

    title: Annotated[
        str,
        Field(description="Название задачи", examples=["abc"]),
    ]

    description: Annotated[
        str | None,
        Field(description="Описание задачи", examples=["abc"]),
    ]

    urgency: Annotated[
        UrgencyTask,
        Field(description="Приоритет задачи", examples=EXAMPLES_URGENCY),
    ]

    order: Annotated[
        Order,
        Field(description="Позиция задачи", examples=[123]),
    ]

    start_at: Annotated[
        dt | None,
        Field(description="Дата начала (UTC)", examples=["2026-05-03T14:00:00Z"]),
    ]

    end_at: Annotated[
        dt | None,
        Field(description="Дата окончания (UTC)", examples=["2026-05-03T15:00:00Z"]),
    ]

    created_at: Annotated[
        dt,
        Field(description="Дата создания (UTC)", examples=["2026-05-03T14:00:00Z"]),
    ]

    updated_at: Annotated[
        dt | None,
        Field(description="Дата обновления (UTC)", examples=["2026-05-03T15:00:00Z"]),
    ]

    model_config = {
        "from_attributes": True,
    }


class CountTaskInBoardResponse(BaseModel):
    """Ответ с количеством задач на доске."""

    board_id: Annotated[
        BoardID,
        Field(description="ID доски", examples=[123]),
    ]

    tasks_count: Annotated[
        NonNegativeInt,
        Field(description="Количество задач на доске", examples=[123]),
    ]

    model_config = {
        "from_attributes": True,
    }


class CountTaskInColumnResponse(BaseModel):
    """Ответ с количеством задач в колонке."""

    column_id: Annotated[
        ColumnID,
        Field(description="ID колонки", examples=[123]),
    ]

    tasks_count: Annotated[
        NonNegativeInt,
        Field(description="Количество задач в колонке", examples=[123]),
    ]

    model_config = {
        "from_attributes": True,
    }
