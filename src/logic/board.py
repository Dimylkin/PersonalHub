from typing import Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.postgres.session import get_session
from database.postgres.dao.board import BoardDAO
from logic.base import BaseLogic
from interfaces.validation.task import CountTaskInBoardResponse


class BoardLogic(BaseLogic):
    dao: BoardDAO
    
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
    
    async def count_tasks_by_board_id(self, board_id: int) -> CountTaskInBoardResponse:
        count =  await self.dao.count_tasks_by_board_id(board_id)
    
        return CountTaskInBoardResponse(
            board_id=board_id,
            tasks_count=count
        )

    async def count_tasks_for_all_boards(self) -> list[CountTaskInBoardResponse]:
        rows = await self.dao.count_tasks_for_all_boards()
    
        return [
                CountTaskInBoardResponse(board_id=board_id, tasks_count=tasks_count)
                for board_id, tasks_count in rows
            ]