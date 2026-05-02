from datetime import datetime as dt

from sqlalchemy import Integer, ForeignKey, Enum, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.postgres.tables.base import TableEntities
from entities.enums import UrgencyTask


class TaskDB(TableEntities):
    __tablename__ = "tasks"

    column_id: Mapped[int] = mapped_column(
        ForeignKey("columns.id", ondelete="CASCADE"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    urgency: Mapped[UrgencyTask] = mapped_column(
        Enum(UrgencyTask),
        nullable=False,
    )

    order: Mapped[int] = mapped_column(Integer, nullable=False)

    start_at: Mapped[dt | None] = mapped_column(DateTime, nullable=True)
    end_at: Mapped[dt | None] = mapped_column(DateTime, nullable=True)

    column: Mapped["ColumnDB"] = relationship(back_populates="tasks")