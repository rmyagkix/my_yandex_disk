from typing import Optional
import datetime
from starlette.responses import JSONResponse
from db import items
from db.histories import histories
from models.item import Item, TreeItems
from .base import BaseRepository


class ItemRepository(BaseRepository):
    async def create(self, i: Item, updateDate: datetime.datetime):
        """Создает или обновляет Item"""
        item = Item(
            id=i.id,
            parentId=i.parentId,
            type=i.type.value,
            url=i.url,
            size=i.size,
        )
        if not updateDate or not item.id or not item.type or (item.type.name == 'FOLDER' and (item.url or item.size)):
            return JSONResponse(
                status_code=400,
                content={"message": "Validation Failed"},
            )
        values = {**item.dict(), 'date': updateDate.isoformat().split('+')[0] + 'Z'}
        query = items.select().where(items.c.id == item.id)
        in_base_item = await self.database.fetch_one(query)  # Поиск эелемента в базе
        if not in_base_item:  # В случае отсутсвие добавление нового
            if not await self.find_parent(item, size=item.size, date=values['date']):
                return JSONResponse(
                    status_code=400,
                    content={"message": "Validation Failed"},
                )
            query = items.insert().values(**values)
            temp = await self.database.execute(query)
            query_hist = histories.insert().values(**values)
            await self.database.execute(query_hist)
            return temp
        else:  # Обновление имеющегося
            in_base_item = Item.parse_obj(in_base_item)
            if item.size and in_base_item.size:
                await self.find_parent(item, size=item.size - in_base_item.size, date=values['date'])
            query = items.update().where(items.c.id == item.id).values(**values)
            query_hist = histories.insert().values(**values)
            temp = await self.database.execute(query)
            await self.database.execute(query_hist)
            return temp

    async def find_parent(self, item: Item, size: Optional[int], date):
        """Ф-я дял поиска родительских элементов до корневого, обновление даты и размера родителей"""
        if item.parentId:
            query = items.select().where(items.c.id == item.parentId)
            parent = await self.database.fetch_one(query)
            if not parent or Item.parse_obj(parent).type.name == 'FILE':
                return False
            parent_i = Item.parse_obj(parent)
            if size:
                if parent_i.size:
                    parent_i.size += size
                else:
                    parent_i.size = size
            values_p = {**parent_i.dict(), 'date': date}
            query_hist = histories.insert().values(**values_p)
            await self.database.execute(query_hist)
            query = items.update().where(items.c.id == parent_i.id).values(**values_p)
            await self.database.execute(query)
            await self.find_parent(parent_i, size, date)
        return True

    async def delete_item(self, id_item: str, date: str):
        """Удаление элемента, его потомков и истории о них"""
        try:
            datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
        except:
            return JSONResponse(
                status_code=400,
                content={"message": "Validation Failed"},
            )

        query = items.select().where(items.c.id == id_item)
        item = await self.database.fetch_one(query)
        if item:
            item: Item = Item.parse_obj(item)
            if item.size:
                await self.find_parent(item, size=-item.size, date=date)
            else:
                await self.find_parent(item, size=None, date=date)
            query = items.delete().where(items.c.id == id_item)
            return await self.database.execute(query)
        return JSONResponse(
            status_code=404,
            content={"message": "Item not found"},
        )

    async def get_items(self, root_item_id: str):
        """Составление дерева наследования для элемента"""
        query = items.select().where(items.c.id == root_item_id)
        item = await self.database.fetch_one(query)
        if not item:
            return JSONResponse(
                status_code=404,
                content={"message": "Item not found"},
            )
        item: TreeItems = TreeItems.parse_obj(item)
        root_item = TreeItems(
            id=item.id,
            parentId=item.parentId,
            type=item.type.value,
            url=item.url,
            size=item.size,
            date=item.date,
            children=None if item.type.name == 'FILE' else await self.find_children(item.id)
        )
        return root_item

    async def find_children(self, root_id) -> list:
        """Ф-я дял поиска потомков элемента"""
        child_list = []
        query = items.select().where(items.c.parentId == root_id)
        child_items = await self.database.fetch_all(query)
        for i in child_items:
            i = TreeItems.parse_obj(i)
            new_root_item = TreeItems(
                id=i.id,
                parentId=i.parentId,
                type=i.type.value,
                url=i.url,
                size=i.size,
                date=i.date,
                children=None if i.type.name == 'FILE' else await self.find_children(i.id)
            )
            child_list.append(new_root_item)
        return child_list
