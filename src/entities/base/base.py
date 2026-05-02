from pydantic import BaseModel
from datetime import datetime as dt

class BaseEntity(BaseModel):
    id: int | None = None
    created_at: dt | None = None
    updated_at: dt | None = None
