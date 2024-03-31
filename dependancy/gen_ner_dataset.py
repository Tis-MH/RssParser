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

# class Info(SQLModel, table=True):
#     entity_title: str
#     title: str
#     episode: int
#     season: str
    


class Database:
    def __init__(self) -> None:
        sqlite_file_name = 'sqlite3.sql'
        sqlite_url = f"sqlite:///{sqlite_file_name}"
        self.engine = create_engine(sqlite_url)
        SQLModel.metadata.create_all(self.engine)
        self.session = Session(self.engine)
        
    def iter_entity(self):
        exection = select(Entity)
        for i in exection:
            print(i)
            
db = Database()
db.iter_entity()