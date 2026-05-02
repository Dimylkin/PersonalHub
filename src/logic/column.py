from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from interfaces.dependencies.session import get_session
from database.postgres.dao.column import ColumnDAO
from logic.base import BaseLogic


class ColumnLogic(BaseLogic):
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
