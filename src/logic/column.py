from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.postgres.session import get_session
from database.postgres.dao.column import ColumnDAO
from interfaces.validation.task import CountTaskInColumnResponse
from logic.base import BaseLogic


class ColumnLogic(BaseLogic):
    dao: ColumnDAO

    @classmethod
    def new_classic(cls):
        async def dependency(
            session: AsyncSession = Depends(get_session),
        ):
            return cls(ColumnDAO(session))

        return dependency

    @classmethod
    def new_tx(cls):
        async def dependency(
            session: AsyncSession = Depends(get_session),
        ):
            return cls(ColumnDAO(session))

        return dependency
    
    async def count_tasks_by_column_id(self, column_id: int) -> CountTaskInColumnResponse:
        count = await self.dao.count_tasks_by_column_id(column_id)
        
        return CountTaskInColumnResponse(
            column_id=column_id,
            tasks_count=count
        )

    async def count_tasks_for_all_columns(self) ->  list[CountTaskInColumnResponse]:
        rows = await self.dao.count_tasks_for_all_columns()

        return [
            CountTaskInColumnResponse(column_id=column_id, tasks_count=tasks_count)
            for column_id, tasks_count in rows
        ]
