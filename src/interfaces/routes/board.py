from fastapi import APIRouter, Depends, HTTPException, status, Response

from interfaces.openapi import OpenAPITags
from logic.board import BoardLogic
from interfaces.validation.board import BoardCreateRequest, BoardUpdateRequest


router = APIRouter(
    prefix="/boards",
    tags=[OpenAPITags.BOARD],
)


@router.get(
    path="/{board_id}",
    summary="Получить доску по ID",
)
async def board_get_by_id(
    board_id: int,
    board_service: BoardLogic = Depends(BoardLogic.new_classic()),
):
    board = await board_service.get_by_id(board_id)

    if board is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found",
        )

    return board


@router.get(
    path="",
    summary="Получить список досок",
)
async def board_get_all(
    board_service: BoardLogic = Depends(BoardLogic.new_classic()),
):
    return await board_service.get_all()


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    summary="Создать доску",
)
async def board_create(
    request: BoardCreateRequest,
    board_service: BoardLogic = Depends(BoardLogic.new_tx()),
):
    return await board_service.create(
        request.model_dump(exclude_none=True),
    )


@router.patch(
    path="/{board_id}",
    summary="Обновить доску",
)
async def board_update(
    board_id: int,
    request: BoardUpdateRequest,
    board_service: BoardLogic = Depends(BoardLogic.new_tx()),
):
    board = await board_service.update(
        entity_id=board_id,
        data=request.model_dump(exclude_none=True),
    )

    if board is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Board not found",
        )

    return board


@router.delete(
    path="/{board_id}",
    summary="Удалить доску",
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT,
)
async def board_delete(
    board_id: int,
    board_service: BoardLogic = Depends(BoardLogic.new_tx()),
):
    await board_service.delete(board_id)
