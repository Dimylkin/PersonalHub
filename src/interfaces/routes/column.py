from fastapi import APIRouter, Depends, Response, status

from exceptions.common import NotFoundObjectException
from interfaces.dependencies.identifier import ColumnID
from interfaces.openapi import OpenAPITags, api_response
from interfaces.validation.column import (
    ColumnCreateRequest,
    ColumnResponse,
    ColumnUpdateRequest,
)
from interfaces.validation.task import CountTaskInColumnResponse
from logic.column import ColumnLogic


router = APIRouter(
    prefix="/columns",
    tags=[OpenAPITags.COLUMN],
)


@router.get(
    path="/{column_id}",
    response_model=ColumnResponse,
    responses=api_response(
        description="Колонка успешно получена",
        errors=[NotFoundObjectException],
    ),
    summary="Получить колонку",
    description="Возвращает данные колонки по её идентификатору.",
)
async def column_get_by_id(
    column_id: ColumnID,
    column_service: ColumnLogic = Depends(ColumnLogic.new_classic()),
):
    """Получает одну колонку по ID."""
    return await column_service.get_by_id(column_id)


@router.get(
    path="",
    response_model=list[ColumnResponse],
    responses=api_response(
        description="Список колонок успешно получен",
    ),
    summary="Получить список колонок",
    description="Возвращает список всех доступных колонок.",
)
async def column_get_all(
    column_service: ColumnLogic = Depends(ColumnLogic.new_classic()),
):
    """Получает список колонок."""
    return await column_service.get_all()


@router.get(
    path="/{column_id}/tasks/count",
    response_model=CountTaskInColumnResponse,
    responses=api_response(
        description="Количество задач в колонке успешно получено",
        errors=[NotFoundObjectException],
    ),
    summary="Получить количество задач в колонке",
    description="Возвращает количество задач, связанных с указанной колонкой.",
)
async def column_tasks_count(
    column_id: ColumnID,
    column_service: ColumnLogic = Depends(ColumnLogic.new_classic()),
) -> CountTaskInColumnResponse:
    """Получает количество задач в колонке."""
    return await column_service.count_tasks_by_column_id(column_id)


@router.get(
    path="/tasks/count",
    response_model=list[CountTaskInColumnResponse],
    responses=api_response(
        description="Количество задач по всем колонкам успешно получено",
    ),
    summary="Получить количество задач по всем колонкам",
    description="Возвращает количество задач, сгруппированное по каждой колонке.",
)
async def columns_tasks_count(
    column_service: ColumnLogic = Depends(ColumnLogic.new_classic()),
) -> list[CountTaskInColumnResponse]:
    """Получает количество задач по всем колонкам."""
    return await column_service.count_tasks_for_all_columns()


@router.post(
    path="",
    response_model=ColumnResponse,
    status_code=status.HTTP_201_CREATED,
    responses=api_response(
        description="Колонка успешно создана",
        status_code=status.HTTP_201_CREATED,
    ),
    summary="Создать колонку",
    description="Создаёт новую колонку на указанной доске.",
)
async def column_create(
    request: ColumnCreateRequest,
    column_service: ColumnLogic = Depends(ColumnLogic.new_tx()),
):
    """Создаёт новую колонку."""
    return await column_service.create(
        request.model_dump(exclude_none=True),
    )


@router.patch(
    path="/{column_id}",
    response_model=ColumnResponse,
    responses=api_response(
        description="Колонка успешно обновлена",
        errors=[NotFoundObjectException],
    ),
    summary="Обновить колонку",
    description="Обновляет данные колонки по её идентификатору.",
)
async def column_update(
    column_id: ColumnID,
    request: ColumnUpdateRequest,
    column_service: ColumnLogic = Depends(ColumnLogic.new_tx()),
):
    """Обновляет колонку по ID."""
    return await column_service.update(
        entity_id=column_id,
        data=request.model_dump(exclude_none=True),
    )


@router.delete(
    path="/{column_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    responses=api_response(
        description="Колонка успешно удалена",
        status_code=status.HTTP_204_NO_CONTENT,
        errors=[NotFoundObjectException],
    ),
    summary="Удалить колонку",
    description="Удаляет колонку по её идентификатору.",
)
async def column_delete(
    column_id: ColumnID,
    column_service: ColumnLogic = Depends(ColumnLogic.new_tx()),
):
    """Удаляет колонку по ID."""
    await column_service.delete(column_id)
