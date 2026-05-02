from dataclasses import dataclass

from entities.base import BaseEntity
from entities.enums import WorkspaceType


@dataclass(slots=True)
class BoardDC(BaseEntity):
    workspace: WorkspaceType
