from fastapi import APIRouter, Depends, HTTPException, status

from interfaces.openapi.tags import OpenAPITags
from logic.column import ColumnLogic
from interfaces.validation.column import (
    ColumnCreateRequest,
    ColumnUpdateRequest,
    ColumnResponse,
)


router = APIRouter(
    prefix="/columns",
    tags=[OpenAPITags.COLUMN],
)


@router.get(
    "/{column_id}",
    response_model=ColumnResponse,
)
async def column_get_by_id(
    column_id: int,
    column_service: ColumnLogic = Depends(ColumnLogic.new_classic()),
):
    column = await column_service.get_by_id(column_id)

    if column is None:
        raise HTTPException(status_code=404, detail="Column not found")

    return column


@router.get(
    "",
    response_model=list[ColumnResponse],
)
async def column_get_all(
    column_service: ColumnLogic = Depends(ColumnLogic.new_classic()),
):
    return await column_service.get_all()


@router.post(
    "",
    response_model=ColumnResponse,
    status_code=status.HTTP_201_CREATED,
)
async def column_create(
    request: ColumnCreateRequest,
    column_service: ColumnLogic = Depends(ColumnLogic.new_tx()),
):
    return await column_service.create(
        request.model_dump(exclude_none=True),
    )


@router.patch(
    "/{column_id}",
    response_model=ColumnResponse,
)
async def column_update(
    column_id: int,
    request: ColumnUpdateRequest,
    column_service: ColumnLogic = Depends(ColumnLogic.new_tx()),
):
    column = await column_service.update(
        entity_id=column_id,
        data=request.model_dump(exclude_none=True),
    )

    if column is None:
        raise HTTPException(status_code=404, detail="Column not found")

    return column


@router.delete(
    "/{column_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def column_delete(
    column_id: int,
    column_service: ColumnLogic = Depends(ColumnLogic.new_tx()),
):
    await column_service.delete(column_id)
