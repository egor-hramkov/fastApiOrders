from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.items.exceptions import ItemAlreadyExistsException
from apps.items.models import Item
from apps.items.schemas import ItemSchema
from apps.user.utils import ExceptionParser
from apps.utils.helpers import SchemaMapper
from database.sql_alchemy import async_session


class ItemRepository:
    """Репозиторий для работы с товаром"""
    session: AsyncSession = async_session

    async def get(self, item_id: int) -> Item:
        """Получение товара"""
        async with self.session() as db:
            statement = select(Item).filter(Item.id == item_id)
            item = await db.execute(statement)
        return item.scalars().first()

    async def get_items(self, ids: list[int]) -> list[Item]:
        """Получение множества товаров"""
        async with self.session() as db:
            statement = select(Item).filter(Item.id.in_(ids))
            items = await db.execute(statement)
        return items.scalars().all()

    async def update(self, item_id: int, new_item: ItemSchema) -> Item:
        """Обновление товара"""
        item = await self.__build_item(new_item, item_id)
        await self.__save(item)
        return item

    async def create(self, item: ItemSchema) -> Item:
        """Создание товара"""
        new_item = await self.__build_item(item)
        await self.__save(new_item)
        return new_item

    async def delete(self, item_id: int) -> None:
        async with self.session() as db:
            item = await self.get(item_id)
            await db.delete(item)
            await db.commit()

    async def __save(self, item: Item) -> None:
        """Сохраняет пользователя в БД"""
        async with self.session() as db:
            try:
                db.add(item)
                await db.commit()
                await db.refresh(item)
            except IntegrityError as e:
                value = ExceptionParser.parse_item_unique_exception(e)
                raise ItemAlreadyExistsException(value)

    async def __build_item(self, item_data: ItemSchema, item_id: int = None) -> Item:
        """Собирает модель товара"""
        if item_id is None:
            item = Item()
        else:
            item = await self.get(item_id)
        mapper = SchemaMapper(item_data, item)
        new_item: Item = mapper.py_to_db_model()
        return new_item
