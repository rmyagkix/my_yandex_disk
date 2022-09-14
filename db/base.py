from databases import Database
from sqlalchemy import create_engine, MetaData
from core.config import DATABASE_URL

database = Database("postgresql://admin:admin@0.0.0.0:32701/yandex_disk")
metadata = MetaData()
engine = create_engine(
    "postgresql://admin:admin@0.0.0.0:32701/yandex_disk",
)
