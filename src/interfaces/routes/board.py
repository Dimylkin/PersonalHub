from fastapi import APIRouter, Depends, Response, status

from exceptions.common import NotFoundObjectException
from interfaces.dependencies.identifier import BoardID
from interfaces.openapi import OpenAPITags, api_response
from interfaces.validation.board import BoardCreateRequest, BoardResponse, BoardUpdateRequest
from interfaces.validation.task import CountTaskInBoardResponse
from logic.board import BoardLogic


router = APIRouter(
    prefix="/boards",
    tags=[OpenAPITags.BOARD],
)


@router.get(
    path="/{board_id}",
    response_model=BoardResponse,
    responses=api_response(
        description="Доска успешно получена",
        errors=[NotFoundObjectException],
    ),
    summary="Получить доску",
    description="Возвращает данные доски по её идентификатору.",
)
async def board_get_by_id(
    board_id: BoardID,
    board_service: BoardLogic = Depends(BoardLogic.new_classic()),
):
    """Получает одну доску по ID."""
    return await board_service.get_by_id(board_id)


@router.get(
    path="",
    response_model=list[BoardResponse],
    responses=api_response(
        description="Список досок успешно получен",
    ),
    summary="Получить список досок",
    description="Возвращает список всех доступных досок.",
)
async def board_get_all(
    board_service: BoardLogic = Depends(BoardLogic.new_classic()),
):
    """Получает список досок."""
    return await board_service.get_all()


@router.get(
    path="/tasks/count",
    response_model=list[CountTaskInBoardResponse],
    responses=api_response(
        description="Количество задач по всем доскам успешно получено",
    ),
    summary="Получить количество задач по всем доскам",
    description="Возвращает количество задач, сгруппированное по каждой доске.",
)
async def boards_tasks_count(
    board_service: BoardLogic = Depends(BoardLogic.new_classic()),
) -> list[CountTaskInBoardResponse]:
    """Получает количество задач по всем доскам."""
    return await board_service.count_tasks_for_all_boards()



@router.get(
    path="/{board_id}/tasks/count",
    response_model=CountTaskInBoardResponse,
    responses=api_response(
        description="Количество задач на доске успешно получено",
        errors=[NotFoundObjectException],
    ),
    summary="Получить количество задач на доске",
    description="Возвращает количество задач, связанных с указанной доской.",
)
async def board_tasks_count(
    board_id: BoardID,
    board_service: BoardLogic = Depends(BoardLogic.new_classic()),
) -> CountTaskInBoardResponse:
    """Получает количество задач на конкретной доске."""
    return await board_service.count_tasks_by_board_id(board_id)


@router.post(
    path="",
    response_model=BoardResponse,
    status_code=status.HTTP_201_CREATED,
    responses=api_response(
        description="Доска успешно создана",
        status_code=status.HTTP_201_CREATED,
    ),
    summary="Создать доску",
    description="Создаёт новую доску в указанном рабочем пространстве.",
)
async def board_create(
    request: BoardCreateRequest,
    board_service: BoardLogic = Depends(BoardLogic.new_tx()),
):
    """Создаёт новую доску."""
    return await board_service.create(
        request.model_dump(exclude_none=True),
    )


@router.patch(
    path="/{board_id}",
    response_model=BoardResponse,
    responses=api_response(
        description="Доска успешно обновлена",
        errors=[NotFoundObjectException],
    ),
    summary="Обновить доску",
    description="Обновляет данные доски по её идентификатору.",
)
async def board_update(
    board_id: BoardID,
    request: BoardUpdateRequest,
    board_service: BoardLogic = Depends(BoardLogic.new_tx()),
):
    """Обновляет доску по ID."""
    return await board_service.update(
        entity_id=board_id,
        data=request.model_dump(exclude_none=True),
    )


@router.delete(
    path="/{board_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    responses=api_response(
        description="Доска успешно удалена",
        status_code=status.HTTP_204_NO_CONTENT,
        errors=[NotFoundObjectException],
    ),
    summary="Удалить доску",
    description="Удаляет доску по её идентификатору.",
)
async def board_delete(
    board_id: BoardID,
    board_service: BoardLogic = Depends(BoardLogic.new_tx()),
):
    """Удаляет доску по ID."""
    await board_service.delete(board_id)
