from pydantic import BaseModel

from entities.enums import WorkspaceType


class BoardCreateRequest(BaseModel):
    workspace: WorkspaceType


class BoardUpdateRequest(BaseModel):
    workspace: WorkspaceType | None = None