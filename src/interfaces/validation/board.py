from typing import Annotated

from pydantic import BaseModel, Field

from entities.enums import WorkspaceType
from interfaces.dependencies.identifier import BoardID


EXAMPLES_TYPE_COLUMN = [e.value for e in WorkspaceType]

class BoardResponse(BaseModel):
    """Ответ с данными доски."""

    id: Annotated[
        BoardID,
        Field(
            description="Уникальный идентификатор доски",
            examples=[123],
        ),
    ]

    workspace: Annotated[
        WorkspaceType,
        Field(
            description="Тип рабочего пространства, к которому принадлежит доска",
            examples=EXAMPLES_TYPE_COLUMN,
        ),
    ]

    model_config = {
        "from_attributes": True,
    }


class BoardCreateRequest(BaseModel):
    """Запрос на создание доски."""

    workspace: Annotated[
        WorkspaceType,
        Field(
            description="Тип рабочего пространства для новой доски",
            examples=EXAMPLES_TYPE_COLUMN,
        ),
    ]


class BoardUpdateRequest(BaseModel):
    """Запрос на обновление доски."""

    workspace: Annotated[
        WorkspaceType | None,
        Field(
            description="Новый тип рабочего пространства",
            examples=EXAMPLES_TYPE_COLUMN,
        ),
    ] = None
