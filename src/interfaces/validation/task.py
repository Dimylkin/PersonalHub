from datetime import datetime as dt

from pydantic import BaseModel

from entities.enums import UrgencyTask


class TaskCreateRequest(BaseModel):
    column_id: int
    title: str
    description: str | None = None
    urgency: UrgencyTask
    order: int
    start_at: dt | None = None
    end_at: dt | None = None


class TaskUpdateRequest(BaseModel):
    column_id: int | None = None
    title: str | None = None
    description: str | None = None
    urgency: UrgencyTask | None = None
    order: int | None = None
    start_at: dt | None = None
    end_at: dt | None = None


class TaskResponse(BaseModel):
    id: int
    column_id: int
    title: str
    description: str | None
    urgency: UrgencyTask
    order: int
    start_at: dt | None
    end_at: dt | None
    created_at: dt
    updated_at: dt | None

    model_config = {
        "from_attributes": True,
    }
