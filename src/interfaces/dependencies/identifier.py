from typing import Annotated

from fastapi import Path
from pydantic import NonNegativeInt, PositiveInt

BoardID = Annotated[
    PositiveInt,
    Path(
        description="Уникальный идентификатор доски",
        examples=[123],
    ),
]

ColumnID = Annotated[
    PositiveInt,
    Path(
        description="Уникальный идентификатор колонки",
        examples=[123],
    ),
]

TaskID = Annotated[
    PositiveInt,
    Path(
        description="Уникальный идентификатор задачи",
        examples=[123],
    ),
]

Order = Annotated[
    NonNegativeInt,
    Path(
        description="Позиция элемента",
        examples=[123],
    ),
]
