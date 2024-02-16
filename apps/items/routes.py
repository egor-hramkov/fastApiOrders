from fastapi import APIRouter

from apps.items.schemas import ItemSchema
from apps.items.service import ItemService

router = APIRouter(
    prefix="/items",
    tags=["items"],
)

service = ItemService()


@router.post("/create", response_model=ItemSchema)
async def create_item(item: ItemSchema):
    """Создание товара"""
    item = await service.create_item(item)
    return item


@router.get("/{item_id}", response_model=ItemSchema)
async def get_item(item_id: int):
    """Получение информации о товаре"""
    item = await service.get_item(item_id)
    return item


@router.get('/get-list/{item_ids}', response_model=list[ItemSchema])
async def get_items(item_ids: str):
    """Получение списка товаров"""
    ids_list = [int(item_id) for item_id in item_ids.split(",")]
    items = await service.get_items(ids_list)
    return items


@router.put("/{item_id}", response_model=ItemSchema)
async def update_item(item_id: int, item: ItemSchema):
    """Обновление товара"""
    item = await service.update_item(item_id, item)
    return item


@router.delete("/{item_id}")
async def delete_item(item_id: int):
    """Удаление товара"""
    return await service.delete_item(item_id)
