import datetime

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, validator, constr
from typing import Optional, List, Union

from starlette.responses import JSONResponse

from db.items import ItemType


class Item(BaseModel):
    id: str = None
    parentId: Optional[str] = None
    type: ItemType = None
    url: Optional[str]
    size: Optional[int]

    @validator('url')
    def url_valid(cls, v, values, **kwargs):
        if len(str(v)) < 256:
            return v
        return JSONResponse(
            status_code=400,
            content={"message": "Validation Failed"},
        )

    @validator('size')
    def size_valid(cls, v, values, **kwargs):
        if v:
            if int(v) >= 0:
                return v
            return JSONResponse(
                status_code=400,
                content={"message": "Validation Failed"},
            )


class ItemsImport(BaseModel):
    items: List[Item]
    updateDate: datetime.datetime = None


class TreeItems(BaseModel):
    id: str
    parentId: Optional[str]
    type: ItemType
    url: Optional[str]
    size: Optional[int]
    date: str
    children: Optional[List['TreeItems']]
