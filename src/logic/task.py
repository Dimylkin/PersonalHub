from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.postgres.session import get_session
from database.postgres.dao.task import TaskDAO
from logic.base import BaseLogic


class TaskLogic(BaseLogic):
    @classmethod
    def new_classic(cls):
        async def dependency(
            session: AsyncSession = Depends(get_session),
        ):
            return cls(TaskDAO(session))

        return dependency

    @classmethod
    def new_tx(cls):
        async def dependency(
            session: AsyncSession = Depends(get_session),
        ):
            return cls(TaskDAO(session))

        return dependency