from fastapi import APIRouter, Depends, HTTPException, status

from interfaces.openapi.tags import OpenAPITags
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
    "/{task_id}",
    response_model=TaskResponse,
)
async def task_get_by_id(
    task_id: int,
    task_service: TaskLogic = Depends(TaskLogic.new_classic()),
):
    task = await task_service.get_by_id(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.get(
    "",
    response_model=list[TaskResponse],
)
async def task_get_all(
    task_service: TaskLogic = Depends(TaskLogic.new_classic()),
):
    return await task_service.get_all()


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def task_create(
    request: TaskCreateRequest,
    task_service: TaskLogic = Depends(TaskLogic.new_tx()),
):
    return await task_service.create(
        request.model_dump(exclude_none=True),
    )


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
)
async def task_update(
    task_id: int,
    request: TaskUpdateRequest,
    task_service: TaskLogic = Depends(TaskLogic.new_tx()),
):
    task = await task_service.update(
        entity_id=task_id,
        data=request.model_dump(exclude_none=True),
    )

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def task_delete(
    task_id: int,
    task_service: TaskLogic = Depends(TaskLogic.new_tx()),
):
    await task_service.delete(task_id)
