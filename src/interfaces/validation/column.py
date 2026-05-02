from pydantic import BaseModel

from entities.enums import TypeColumn
from datetime import datetime as dt

class ColumnCreateRequest(BaseModel):
    board_id: int
    type: TypeColumn
    order: int


class ColumnUpdateRequest(BaseModel):
    board_id: int | None = None
    type: TypeColumn | None = None
    order: int | None = None


class ColumnResponse(BaseModel):
    id: int
    board_id: int
    type: TypeColumn
    order: int
    created_at: dt
    updated_at: dt | None

    model_config = {
        "from_attributes": True
    }