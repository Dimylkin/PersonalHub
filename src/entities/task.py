from dataclasses import dataclass
from datetime import datetime as dt

from entities.base import BaseEntity
from entities.enums import UrgencyTask


@dataclass(slots=True)
class TaskDC(BaseEntity):
    title: str
    description: str | None
    column_id: int
    urgency: UrgencyTask
    order: int
    start_at: dt | None
    end_at: dt | None