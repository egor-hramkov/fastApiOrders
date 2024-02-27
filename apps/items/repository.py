from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.items.exceptions import ItemAlreadyExistsException, ItemDoesNotExistException, ItemsDoesNotExistException
from apps.items.models import Item
from apps.items.schemas import ItemSchema
from apps.utils.exception_parser import ExceptionParser
from apps.utils.helpers import SchemaMapper
from database.sql_alchemy import async_session


class ItemRepository:
    """Репозиторий для работы с товаром"""
    session: AsyncSession = async_session

    async def get_raw_item(self, item_id: int) -> Item:
        """Получение записи товара из БД"""
        async with self.session() as db:
            statement = select(Item).filter(Item.id == item_id)
            item = await db.execute(statement)
        item = item.scalars().first()
        if item is None:
            raise ItemDoesNotExistException()
        return item

    async def get(self, item_id: int) -> ItemSchema:
        """Получение товара"""
        item = await self.get_raw_item(item_id)
        return ItemSchema.model_validate(item, from_attributes=True)

    async def get_items(self, ids: list[int] | set) -> list[ItemSchema]:
        """Получение множества товаров"""
        async with self.session() as db:
            statement = select(Item).filter(Item.id.in_(ids))
            items = await db.execute(statement)
        items = items.scalars().all()
        items_ids = set(item.id for item in items)
        if len(ids) != len(items_ids):
            missing_items = set(ids) - set(items_ids)
            raise ItemsDoesNotExistException(missing_items)
        return [ItemSchema.model_validate(item, from_attributes=True) for item in items]

    async def update(self, item_id: int, new_item: ItemSchema) -> ItemSchema:
        """Обновление товара"""
        item = await self.__build_item(new_item, item_id)
        await self.__save(item)
        return ItemSchema.model_validate(item, from_attributes=True)

    async def create(self, item: ItemSchema) -> ItemSchema:
        """Создание товара"""
        new_item = await self.__build_item(item)
        await self.__save(new_item)
        return ItemSchema.model_validate(new_item, from_attributes=True)

    async def delete(self, item_id: int) -> None:
        async with self.session() as db:
            item = await self.get_raw_item(item_id)
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
                value = ExceptionParser.parse_unique_exception(e, ['name'])
                raise ItemAlreadyExistsException(value)

    async def __build_item(self, item_data: ItemSchema, item_id: int = None) -> Item:
        """Собирает модель товара"""
        if item_id is None:
            item = Item()
        else:
            item = await self.get_raw_item(item_id)
        mapper = SchemaMapper(item_data, item)
        new_item: Item = mapper.py_to_db_model()
        return new_item
