from fastapi import APIRouter
from interfaces.openapi import OpenAPITags


router = APIRouter(
    prefix="/boards",
    tags=[OpenAPITags.BOARD],
)


@router.get(
    "/{board_id}",
)
async def board_get_by_id(board_id: int):
    ...


@router.get(
    "",
)
async def board_get_all():
    ...


@router.post(
    "",
)
async def board_create():
    ...


@router.patch(
    "/{board_id}",
)
async def board_update(board_id: int):
    ...


@router.delete(
    "/{board_id}",
)
async def board_delete(board_id: int):
    ...
