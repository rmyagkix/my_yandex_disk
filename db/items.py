import sqlalchemy
from .base import metadata
import datetime
import enum


class ItemType(enum.Enum):
    FILE = 'FILE'
    FOLDER = 'FOLDER'


items = sqlalchemy.Table(
    'items',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.String, primary_key=True, unique=True),
    sqlalchemy.Column('parentId', sqlalchemy.ForeignKey('items.id', ondelete='CASCADE'), nullable=True),
    sqlalchemy.Column('type', sqlalchemy.Enum(ItemType), default=ItemType.FILE, nullable=False),
    sqlalchemy.Column('url', sqlalchemy.String),
    sqlalchemy.Column('size', sqlalchemy.Integer),
    sqlalchemy.Column('date', sqlalchemy.String, default=datetime.datetime.utcnow().isoformat())

)
