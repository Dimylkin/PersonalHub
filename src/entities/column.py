from dataclasses import dataclass

from entities.base import BaseEntity
from entities.enums import TypeColumn


@dataclass(slots=True)
class ColumnDC(BaseEntity):
    board_id: int
    type: TypeColumn
    order: int   