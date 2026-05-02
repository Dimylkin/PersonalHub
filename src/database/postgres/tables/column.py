from sqlalchemy import Enum, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.postgres.tables.base import TableEntities
from entities.enums import TypeColumn


class ColumnDB(TableEntities):
    __tablename__ = "columns"

    board_id: Mapped[int] = mapped_column(
        ForeignKey("boards.id", ondelete="CASCADE"),
        nullable=False,
    )

    type: Mapped[TypeColumn] = mapped_column(
        Enum(TypeColumn),
        nullable=False,
    )
    
    order: Mapped[int] = mapped_column(Integer, nullable=False)

    board: Mapped["BoardDB"] = relationship(back_populates="columns")

    tasks: Mapped[list["TaskDB"]] = relationship(
        back_populates="column",
        cascade="all, delete-orphan",
    )
