from typing import Any


class BaseLogic:
    def __init__(self, dao):
        self.dao = dao

    async def get_by_id(self, entity_id: int):
        return await self.dao.get_by_id(entity_id)

    async def get_all(self):
        return await self.dao.get_all()

    async def create(self, data: dict[str, Any]):
        return await self.dao.create(data)

    async def update(self, entity_id: int, data: dict[str, Any]):
        return await self.dao.update(entity_id, data)

    async def delete(self, entity_id: int):
        return await self.dao.delete_by_id(entity_id)
