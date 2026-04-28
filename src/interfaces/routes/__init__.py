from fastapi import APIRouter

from .board import router as board_router
from .column import router as column_router
from .task import router as task_router

router = APIRouter()

router.include_router(board_router)
router.include_router(column_router)
router.include_router(task_router)

__all__ = ["router"]
