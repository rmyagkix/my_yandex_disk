from typing import List, Optional

from fastapi import APIRouter, Depends

from models.item import ItemsImport, TreeItems
from repositories.histories import HistoryRepository
from .depends import get_history_repository
from repositories.items import ItemRepository

router = APIRouter()


@router.get('/updates')
async def get_updates(
        date: Optional[str] = None,
        histories: HistoryRepository = Depends(get_history_repository)
):
    return await histories.get_histories_24h(date)


@router.get('/node/{id}/history')
async def get_history_from_to(
        id: str,
        dateStart: Optional[str] = None,
        dateEnd: Optional[str] = None,
        histories: HistoryRepository = Depends(get_history_repository)
):
    return await histories.history_from_to(id, dateStart, dateEnd)
