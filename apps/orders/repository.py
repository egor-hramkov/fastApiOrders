from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from apps.items.repository import ItemRepository
from apps.items.schemas import ItemSchema
from apps.orders.enums import OrderStatusEnum
from apps.orders.exceptions import OrderAlreadyExistsException, OrderDoesNotExistsException
from apps.orders.models import Order, OrderItem
from apps.orders.schemas import OrderSchema, OrderIn
from apps.user.repository import UserRepository
from apps.user.utils import ExceptionParser
from database.sql_alchemy import async_session


class OrderRepository:
    """Репозиторий для работы с заказами"""

    session: AsyncSession = async_session
    _item_repository = ItemRepository()
    _user_repository = UserRepository()

    async def get(self, order_id: int, user_id: int) -> OrderSchema:
        """Получение заказа"""
        async with self.session() as db:
            statement = select(Order).filter(Order.id == order_id)
            result = await db.execute(statement)
            order = result.scalars().first()
        if order is None:
            raise OrderDoesNotExistsException()
        user = await self._user_repository.get_user(user_id)
        items = await self.__get_order_items(order_id)
        order_data = await OrderSchema.build_order_schema(order, user, items)
        return order_data

    async def create(self, order: OrderIn, user_id: int) -> OrderSchema:
        """Создание заказа"""
        new_order = await self.__build_order(user_id)
        await self.__save_order(new_order)
        items = await self.__prepare_items_in_order(order, new_order.id)
        user = await self._user_repository.get_user(user_id)
        order_data = await OrderSchema.build_order_schema(new_order, user, items)
        return order_data

    async def delete(self, order_id: int) -> None:
        """Удаление заказа"""
        async with self.session() as db:
            stmt = delete(Order).where(Order.id == order_id)
            res = await db.execute(stmt)
            if res.rowcount == 0:
                raise OrderDoesNotExistsException()
            await db.commit()

    async def update(self, order: OrderIn) -> OrderSchema:
        """Обновление заказа"""
        ...

    async def __build_order(self, user_id: int) -> Order:
        """Собирает модель заказа"""
        new_order = Order()
        new_order.status = OrderStatusEnum.created
        new_order.user_id = user_id
        return new_order

    async def __link_items_to_an_order(self, items: list[OrderItem]) -> None:
        """Связывает товары с заказом"""
        items_in_order = items
        async with self.session() as db:
            db.add_all(items_in_order)
            await db.commit()
            # await db.refresh(order)

    async def __build_items_links_to_order(self, items: list[ItemSchema], order_id: int) -> list[OrderItem]:
        """Создает сущности связки товар-заказ"""
        items_in_order: list[OrderItem] = []
        for item in items:
            item_in_order = OrderItem()
            item_in_order.order_id = order_id
            item_in_order.item_id = item.id
            items_in_order.append(item_in_order)
        return items_in_order

    async def __save_order(self, order: Order):
        """Сохранение заказа"""
        async with self.session() as db:
            try:
                db.add(order)
                await db.commit()
                await db.refresh(order)
            except IntegrityError as e:
                value = ExceptionParser.parse_order_unique_exception(e)
                raise OrderAlreadyExistsException(value)

    async def __get_order_items(self, order_id: int) -> list[ItemSchema]:
        """Получение товаров в заказе"""
        async with self.session() as db:
            result = await db.execute(select(OrderItem).filter(OrderItem.order_id == order_id))
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
