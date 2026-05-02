from typing import Any, Generic, TypeVar

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.postgres.tables.base import TableEntities


ModelT = TypeVar("ModelT", bound=TableEntities)


class BaseDAO(Generic[ModelT]):
    model: type[ModelT]

    def __init__(self, session: AsyncSession):
        self.session = session

        if self.model is None:
            raise ValueError(f"Model not set for {self.__class__.__name__}")

    async def get_by_id(self, entity_id: int) -> ModelT | None:
        return await self.session.get(self.model, entity_id)

    async def get_all(self) -> list[ModelT]:
        stmt = select(self.model).order_by(self.model.id)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, data: dict[str, Any]) -> ModelT:
        obj = self.model(**data)

        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)

        return obj

    async def update(self, entity_id: int, data: dict[str, Any]) -> ModelT | None:
        obj = await self.get_by_id(entity_id)

        if obj is None:
            return None

        for field, value in data.items():
            setattr(obj, field, value)

        await self.session.flush()
        await self.session.refresh(obj)

        return obj

    async def delete_by_id(self, entity_id: int) -> None:
        obj = await self.get_by_id(entity_id)

        if obj is None:
            return

        await self.session.delete(obj)
        await self.session.flush()