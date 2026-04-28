from fastapi import APIRouter
from interfaces.openapi.tags import OpenAPITags


router = APIRouter(
    prefix="/columns",
    tags=[OpenAPITags.COLUMN],
)


@router.get(
    "/{column_id}",
)
async def column_get_by_id(column_id: int):
    ...


@router.get(
    "",
)
async def column_get_all(
    board_id: int | None = None,  # фильтр по доске
):
    ...


@router.post(
    "",
)
async def column_create():
    ...


@router.patch(
    "/{column_id}",
)
async def column_update(column_id: int):
    ...


@router.delete(
    "/{column_id}",
)
async def column_delete(column_id: int):
    ...
