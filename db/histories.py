import sqlalchemy
from .base import metadata
import datetime

from .items import ItemType

histories = sqlalchemy.Table(
    'histories',
    metadata,
    sqlalchemy.Column('idUnit', sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column('id', sqlalchemy.ForeignKey('items.id', ondelete='CASCADE'), nullable=True),
    sqlalchemy.Column('parentId', sqlalchemy.String),
    sqlalchemy.Column('type', sqlalchemy.Enum(ItemType)),
    sqlalchemy.Column('url', sqlalchemy.String),
    sqlalchemy.Column('size', sqlalchemy.Integer),
    sqlalchemy.Column('date', sqlalchemy.String, default=datetime.datetime.utcnow().isoformat())
)
