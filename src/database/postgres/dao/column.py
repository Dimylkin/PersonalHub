from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.postgres.dao.base import BaseDAO
from database.postgres.tables.column import ColumnDB
from database.postgres.tables.task import TaskDB


class ColumnDAO(BaseDAO[ColumnDB]):
    model = ColumnDB

    async def count_tasks_by_column_id(self, column_id: int) -> int:
        stmt = (
            select(func.count(TaskDB.id))
            .where(TaskDB.column_id == column_id)
        )

        result = await self.session.execute(stmt)
        return result.scalar_one()
    
    async def count_tasks_for_all_columns(self) -> Sequence[tuple[int, int]]:
        stmt = (
            select(
                TaskDB.column_id,
                func.count(TaskDB.id).label("tasks_count"),
            )
            .group_by(TaskDB.column_id)
        )

        result = await self.session.execute(stmt)
        return result.all()
