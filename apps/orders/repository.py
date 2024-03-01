from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from apps.items.repository import ItemRepository
from apps.items.schemas import ItemSchema
from apps.orders.enums.order_statuses_enum import OrderStatusEnum
from apps.orders.exceptions import (
    OrderAlreadyExistsException,
    OrderDoesNotExistsException,
    StatusDoesNotExistsException
)
from apps.orders.models import Order, OrderItem
from apps.orders.schemas import OrderSchema, OrderIn, OrderUpdateSchema
from apps.user.repository import UserRepository
from apps.utils.exception_parser import ExceptionParser
from database.sql_alchemy import async_session


class OrderRepository:
    """Репозиторий для работы с заказами"""

    session: AsyncSession = async_session
    _item_repository = ItemRepository()
    _user_repository = UserRepository()

    async def get_order(self, order_id: int) -> OrderSchema:
        """Получение заказа"""
        raw_order = await self.get_raw_order(order_id)
        order = await self.__build_order(raw_order)
        return order

    async def get_raw_order(self, order_id: int) -> Order:
        """Получение записи заказа из БД"""
        async with self.session() as db:
            statement = select(Order).filter(Order.id == order_id)
            result = await db.execute(statement)
            order = result.scalars().first()
        if order is None:
            raise OrderDoesNotExistsException()
        return order

    async def create(self, order: OrderIn, user_id: int) -> OrderSchema:
        """Создание заказа"""
        new_order = Order(status=OrderStatusEnum.created, user_id=user_id)
        await self.__save_order(new_order)
        await self.__prepare_items_in_order(order, new_order.id)
        built_order = await self.__build_order(new_order)
        return built_order

    async def delete_order(self, order_id: int) -> None:
        """Удаление заказа"""
        order = await self.get_raw_order(order_id)
        async with self.session() as db:
            await db.delete(order)
            await db.commit()

    async def update(self, order_id: int, order_data: OrderUpdateSchema) -> OrderSchema:
        """Обновление заказа"""
        order = await self.get_raw_order(order_id)
        old_status = order.status
        await self.update_order_status(order_id, order_data.status)
        await self.__save_order(order)

        new_order_items_ids = set(item.id for item in order_data.items)
        new_order_items = await self._item_repository.get_items(new_order_items_ids)

        items_in_order: list[ItemSchema] = await self.__get_order_items(order_id)
        old_order_items_ids = set(item.id for item in items_in_order)
        items_ids_to_add = new_order_items_ids - old_order_items_ids
        items_ids_to_delete = old_order_items_ids - new_order_items_ids
        await self.add_items_in_order(order.id, items_ids_to_add)
        await self.remove_items_in_order(order.id, items_ids_to_delete)
        return await self.__build_order(order, new_order_items, old_status=old_status)

    async def add_items_in_order(self, order_id: int, items_ids: list | set) -> None:
        """Добавляет товары в заказ"""
        items_in_order = [OrderItem(item_id=item_id, order_id=order_id) for item_id in items_ids]
        async with self.session() as db:
            db.add_all(items_in_order)
            await db.commit()

    async def remove_items_in_order(self, order_id: int, items_ids: list | set) -> None:
        """Удаляет товары из заказа"""
        async with self.session() as db:
            statement = delete(OrderItem).where(
                OrderItem.item_id.in_(items_ids), OrderItem.order_id == order_id
            )
            await db.execute(statement)
            await db.commit()

    async def update_order_status(self, order_id: int, new_status: str) -> OrderSchema:
        """Обновляет статус заказа"""
        if new_status not in OrderStatusEnum:
            raise StatusDoesNotExistsException()
        order = await self.get_raw_order(order_id)
        old_status = order.status
        order.status = new_status
        await self.__save_order(order)
        return await self.__build_order(order, old_status=old_status)

    async def __build_order(
            self,
            order: Order,
            items: list[ItemSchema] = None,
            old_status: OrderStatusEnum = None
    ) -> OrderSchema:
        """Собирает информацию о заказе"""
        user = await self._user_repository.get_user(order.user_id)
        if items is None:
            items = await self.__get_order_items(order.id)
        order_data = await OrderSchema.build_order_schema(order, user, items, old_status=old_status)
        return order_data

    async def __build_items_links_to_order(self, items: list[ItemSchema], order_id: int) -> list[OrderItem]:
        """Создает сущности связки товар-заказ"""
        items_in_order = [OrderItem(order_id=order_id, item_id=item.id) for item in items]
        return items_in_order

    async def __save_order(self, order: Order):
        """Сохранение заказа"""
        async with self.session() as db:
            try:
                db.add(order)
                await db.commit()
                await db.refresh(order)
            except IntegrityError as e:
                value = ExceptionParser.parse_unique_exception(e, ['id'])
                raise OrderAlreadyExistsException(value)

    async def __get_order_items(self, order_id: int) -> list[ItemSchema]:
        """Получение товаров в заказе"""
        async with self.session() as db:
            result = await db.execute(
                select(OrderItem).filter(OrderItem.order_id == order_id)
            )
            order_items = result.scalars().all()
        items_ids = [item.item_id for item in order_items]
        items = await self._item_repository.get_items(items_ids)
        return items

    async def __prepare_items_in_order(self, order: OrderIn, order_id: int) -> list[ItemSchema]:
        """Создаёт связи товаров с заказом"""
        items_ids = [item.id for item in order.items]
        items = await self._item_repository.get_items(items_ids)
        items_in_order = await self.__build_items_links_to_order(items, order_id)
        await self.__link_items_to_an_order(items_in_order)
        return items

    async def __link_items_to_an_order(self, items: list[OrderItem]) -> None:
        """Связывает товары с заказом"""
        items_in_order = items
        async with self.session() as db:
            db.add_all(items_in_order)
            await db.commit()
