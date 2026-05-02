from typing import Any

from sqlalchemy import DateTime, Integer, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime as dt


class BaseDB(DeclarativeBase, AsyncAttrs):
    __abstract__ = True

    def as_dict(
        self,
        exclude_none: bool = False,
        exclude_columns: list[str] | None = None,
    ) -> dict[str, Any]:
        data = {}
        for c in inspect(self).mapper.column_attrs:
            attr = getattr(self, c.key)
            if exclude_columns:
                if c.key in exclude_columns:
                    continue
            if exclude_none:
                if attr is not None:
                    data[c.key] = attr
            else:
                data[c.key] = attr
        return data


class TableEntities(BaseDB):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)

    created_at: Mapped[dt] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[dt | None] = mapped_column(
        DateTime,
        onupdate=func.now(),
        nullable=True,
    )
