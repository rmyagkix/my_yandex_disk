from typing import Optional
import datetime
from starlette.responses import JSONResponse
from db import items
from db.histories import histories
from db.items import ItemType
from models.history import HistoryUnit, HistoryUnitOut
from models.item import Item, TreeItems
from .base import BaseRepository


class HistoryRepository(BaseRepository):
    async def get_histories_24h(self, date):
        if not date:
            return JSONResponse(
                status_code=400,
                content={"message": "Validation Failed"},
            )
        request_date = await self.to_datetime(date)
        query = histories.select().where(histories.c.type == ItemType.FILE)
        all_files = await self.database.fetch_all(query)
        if not all_files:
            return JSONResponse(
                status_code=400,
                content={"message": "Validation Failed"},
            )
        need_items = []
        for f in all_files:
            f = HistoryUnitOut.parse_obj(f)
            if datetime.timedelta(days=1) <= request_date - await self.to_datetime(f.date):
                need_items.append(f)
        return need_items

    @classmethod
    async def to_datetime(cls, date):
        if date:
            return datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
        return None

    async def history_from_to(self, id, dateStart, dateEnd):
        need_items = []
        query = histories.select().where(histories.c.id == id)
        dateStart = await self.to_datetime(dateStart)
        dateEnd = await self.to_datetime(dateEnd)
        all_files = await self.database.fetch_all(query)
        for f in all_files:
            f = HistoryUnitOut.parse_obj(f)
            if dateStart and dateEnd:
                if dateStart <= await self.to_datetime(f.date) < dateEnd:
                    need_items.append(f)
            elif dateStart and not dateEnd:
                if dateStart <= await self.to_datetime(f.date):
                    need_items.append(f)
            elif not dateStart and dateEnd:
                if await self.to_datetime(f.date) < dateEnd:
                    need_items.append(f)
            else:
                need_items.append(f)
        return need_items
