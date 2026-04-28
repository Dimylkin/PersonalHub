from fastapi import APIRouter
from interfaces.openapi.tags import OpenAPITags


router = APIRouter(
    prefix="/tasks",
    tags=[OpenAPITags.TASK],
)


@router.get(
    "/{task_id}",
)
async def task_get_by_id(task_id: int):
    ...


@router.get(
    "",
)
async def task_get_all(
    column_id: int | None = None,
    board_id: int | None = None,
):
    ...


@router.post(
    "",
)
async def task_create():
    ...


@router.patch(
    "/{task_id}",
)
async def task_update(task_id: int):
    ...


@router.delete(
    "/{task_id}",
)
async def task_delete(task_id: int):
    ...
