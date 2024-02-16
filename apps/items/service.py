from apps.items.models import Item
from apps.items.repository import ItemRepository
from apps.items.schemas import ItemSchema


class ItemService:
    """Сервис для работы с товаром"""
    _repository = ItemRepository()

    async def create_item(self, item: ItemSchema) -> Item:
        """Создание товара"""
        return await self._repository.create(item)

    async def get_item(self, item_id: int) -> Item:
        """Получение товара"""
        return await self._repository.get(item_id)

    async def get_items(self, item_ids: list[int]) -> list[Item]:
        """Получение товара"""
        return await self._repository.get_items(item_ids)

    async def update_item(self, item_id: int, item: ItemSchema) -> Item:
        """Обновление товара"""
        return await self._repository.update(item_id, item)

    async def delete_item(self, item_id: int) -> None:
        """Удаление товара"""
        return await self._repository.delete(item_id)
