from typing import Optional

from fastapi import APIRouter, Depends

from models.item import ItemsImport, TreeItems
from .depends import get_item_repository
from repositories.items import ItemRepository

router = APIRouter()


@router.get('/nodes/{id}', response_model=TreeItems)
async def get_tree(
        id: str,
        users: ItemRepository = Depends(get_item_repository)
):
    return await users.get_items(id)


@router.post('/imports')
async def create_item(
        item: ItemsImport,
        items: ItemRepository = Depends(get_item_repository)):
    for i in item.items:
        n_item = await items.create(i=i, updateDate=item.updateDate)
        if n_item:
            return n_item
    return item


@router.delete('/delete/{id}')
async def delete_item(
        id: str,
        date: Optional[str],
        items: ItemRepository = Depends(get_item_repository)):
    return await items.delete_item(id, date)

