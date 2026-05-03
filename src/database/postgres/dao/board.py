from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.postgres.dao.base import BaseDAO
from database.postgres.tables.board import BoardDB
from database.postgres.tables.column import ColumnDB
from database.postgres.tables.task import TaskDB


class BoardDAO(BaseDAO[BoardDB]):
    model = BoardDB

    async def count_tasks_by_board_id(self, board_id: int) -> int:
        await self.get_by_id(board_id)

        stmt = (
            select(func.count(TaskDB.id))
            .join(ColumnDB, TaskDB.column_id == ColumnDB.id)
            .where(ColumnDB.board_id == board_id)
        )

        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def count_tasks_for_all_boards(self) -> Sequence[tuple[int, int]]:
        stmt = (
            select(
                ColumnDB.board_id,
                func.count(TaskDB.id).label("tasks_count"),
            )
            .join(TaskDB, TaskDB.column_id == ColumnDB.id)
            .group_by(ColumnDB.board_id)
        )

        result = await self.session.execute(stmt)
        return result.all()
