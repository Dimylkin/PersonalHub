from typing import Any

from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


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
