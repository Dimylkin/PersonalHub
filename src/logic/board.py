from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from interfaces.dependencies.session import get_session
from database.postgres.dao.board import BoardDAO
from logic.base import BaseLogic


class BoardLogic(BaseLogic):
    @classmethod
    def new_classic(cls):
        async def dependency(
            session: AsyncSession = Depends(get_session),
        ):
            return cls(BoardDAO(session))

        return dependency

    @classmethod
    def new_tx(cls):
        async def dependency(
            session: AsyncSession = Depends(get_session),
        ):
            return cls(BoardDAO(session))

        return dependency
