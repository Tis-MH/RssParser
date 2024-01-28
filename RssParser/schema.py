from sqlmodel import Field, SQLModel, create_engine, Session, select, ForeignKey
from typing import Dict, List, Optional
import datetime

class SubscribeWebsite(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    url: str
    interval: int
    update: bool


class UpdateRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    website_id: int
    update_time: datetime.datetime


class Entity(SQLModel, table=True):
    title: str = Field(primary_key=True)
    magnet: str
    upload_time: Optional[datetime.datetime]
    category: Optional[str]
    size: Optional[str]


class Database:
    def __init__(self) -> None:
        sqlite_file_name = 'sqlite3.sql'
        sqlite_url = f"sqlite:///{sqlite_file_name}"
        self.engine = create_engine(sqlite_url)
        SQLModel.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def get_subscribe(self):
        execution = select(SubscribeWebsite).where(SubscribeWebsite.update == True)
        return self.session.exec(execution)

    def add_subscribe(self, name, url, interval=1440, update=True):
        self.session.add(
            SubscribeWebsite(name=name, url=url, interval=interval, update=update)
        )
        self.session.commit()

    def update_subscribe(self, id, name, url, interval, update):
        execution = select(SubscribeWebsite).where(SubscribeWebsite.id == id)
        entity = self.session.exec(execution).one()
        entity.name = name
        entity.url = url
        entity.interval = interval
        entity.update = update
        self.session.add(entity)
        self.session.commit()

    def delete_subscribe(self, id):
        execution = select(SubscribeWebsite).where(SubscribeWebsite.id == id)
        entity = self.session.exec(execution).one()
        self.session.delete(entity)
        self.session.commit()
