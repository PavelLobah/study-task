# app/db/db.py

import databases
import ormar
import sqlalchemy
from datetime import datetime
from app.settings import get_settings

settings = get_settings()
database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class Task(ormar.Model):
    class Meta(BaseMeta):
        tablename = "tasks"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=255)
    description: str = ormar.String(max_length=255)
    created_at: datetime = ormar.DateTime(default=datetime.utcnow)


engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)
