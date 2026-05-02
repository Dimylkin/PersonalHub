from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.postgres.tables.base import TableEntities
from entities.enums import WorkspaceType


class BoardDB(TableEntities):
    __tablename__ = "boards"

    workspace: Mapped[WorkspaceType] = mapped_column(
        Enum(WorkspaceType),
        nullable=False,
    )
    columns: Mapped[list["ColumnDB"]] = relationship(
        back_populates="board",
        cascade="all, delete-orphan",
    )
