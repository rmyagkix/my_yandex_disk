from pydantic import BaseModel
from typing import Optional
from db.items import ItemType


class HistoryUnit(BaseModel):
    idUnit: int
    id: str = None
    parentId: Optional[str] = None
    type: ItemType
    url: Optional[str]
    size: Optional[int]
    date: str


class HistoryUnitOut(BaseModel):
    id: str = None
    parentId: Optional[str] = None
    type: ItemType
    url: Optional[str]
    size: Optional[int]
    date: str
