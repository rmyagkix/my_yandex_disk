from repositories.histories import HistoryRepository
from repositories.items import ItemRepository
from db.base import database


def get_item_repository() -> ItemRepository:
    return ItemRepository(database)


def get_history_repository() -> HistoryRepository:
    return HistoryRepository(database)
