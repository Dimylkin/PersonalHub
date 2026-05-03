from fastapi import APIRouter, Depends, Response, status

from exceptions.common import NotFoundObjectException
from interfaces.dependencies.identifier import TaskID
from interfaces.openapi import OpenAPITags, api_response
from interfaces.validation.task import (
    TaskCreateRequest,
    TaskResponse,
    TaskUpdateRequest,
)
from logic.task import TaskLogic


router = APIRouter(
    prefix="/tasks",
    tags=[OpenAPITags.TASK],
)


@router.get(
    path="/{task_id}",
    response_model=TaskResponse,
    responses=api_response(
        description="Задача успешно получена",
        errors=[NotFoundObjectException],
    ),
    summary="Получить задачу",
    description="Возвращает данные задачи по её идентификатору.",
)
async def task_get_by_id(
    task_id: TaskID,
    task_service: TaskLogic = Depends(TaskLogic.new_classic()),
):
    """Получает задачу по ID."""
    return await task_service.get_by_id(task_id)


@router.get(
    path="",
    response_model=list[TaskResponse],
    responses=api_response(
        description="Список задач успешно получен",
    ),
    summary="Получить список задач",
    description="Возвращает список всех задач.",
)
async def task_get_all(
    task_service: TaskLogic = Depends(TaskLogic.new_classic()),
):
    """Получает список задач."""
    return await task_service.get_all()


@router.post(
    path="",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    responses=api_response(
        description="Задача успешно создана",
        status_code=status.HTTP_201_CREATED,
    ),
    summary="Создать задачу",
    description="Создаёт новую задачу в указанной колонке.",
)
async def task_create(
    request: TaskCreateRequest,
    task_service: TaskLogic = Depends(TaskLogic.new_tx()),
):
    """Создаёт новую задачу."""
    return await task_service.create(
        request.model_dump(exclude_none=True),
    )


@router.patch(
    path="/{task_id}",
    response_model=TaskResponse,
    responses=api_response(
        description="Задача успешно обновлена",
        errors=[NotFoundObjectException],
    ),
    summary="Обновить задачу",
    description="Обновляет данные задачи по её идентификатору.",
)
async def task_update(
    task_id: TaskID,
    request: TaskUpdateRequest,
    task_service: TaskLogic = Depends(TaskLogic.new_tx()),
):
    """Обновляет задачу по ID."""
    return await task_service.update(
        entity_id=task_id,
        data=request.model_dump(exclude_none=True),
    )


@router.delete(
    path="/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    responses=api_response(
        description="Задача успешно удалена",
        status_code=status.HTTP_204_NO_CONTENT,
        errors=[NotFoundObjectException],
    ),
    summary="Удалить задачу",
    description="Удаляет задачу по её идентификатору.",
)
async def task_delete(
    task_id: TaskID,
    task_service: TaskLogic = Depends(TaskLogic.new_tx()),
):
    """Удаляет задачу по ID."""
    await task_service.delete(task_id)
