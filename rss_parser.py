import asyncio
import datetime
import httpx
import feedparser
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session, select
import json
from pprint import pprint
from sqlmodel import Field, SQLModel, create_engine, Session, ForeignKey


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
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    magnet: str
    upload_time: Optional[datetime.datetime]
    category: Optional[str]
    size: Optional[str]


class Parser():
    link: str
    xml: str
    entity: dict
        
    def __init__(self, link) -> None:
        self.link = link
    
    def client(self):
        return httpx.AsyncClient(proxy="http://localhost:7890")
        
    async def get(self):
        async with self.client() as client:
            res = await client.get(self.link)
            self.xml = res.text
            
    def html_parser(self):
        self.entity = feedparser.parse(self.xml)

    async def parser(self):
        await self.get()
        self.html_parser()
        return self.entity
    
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
        entity.update= update
        self.session.add(entity)
        self.session.commit()
        
    def delete_subscribe(self, id):
        execution = select(SubscribeWebsite).where(SubscribeWebsite.id == id)
        entity = self.session.exec(execution).one()
        self.session.delete(entity)
        self.session.commit()
        
    

    
class Crawler:
    def __init__(self) -> None:
        self.database = Database()
        
    async def update_subscribe(self):
        li = []
        for entity in self.database.get_subscribe():
            li.append({
                'id': entity.id,
                'entity': entity,
                'parser': Parser(entity.url),
            })
        
        res = await asyncio.gather(*[i['parser'].parser() for i in li])
        print(res)
        return res
    
# par1 = Parser('https://nyaa.si/?page=rss')
# par2 = Parser('https://share.acgnx.se/rss.xml')

if __name__ == "__main__":
    db = Database()
    for i in db.get_subscribe():
            print(i)
    # db.delete_subscribe(2)
    # db.add_subscribe('nyaa', 'https://nyaa.si/?page=rss')
    # db.add_subscribe('acgnx', 'https://share.acgnx.se/rss.xml')