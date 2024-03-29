import asyncio
import datetime
from inspect import isclass
import itertools
import httpx
import feedparser

import json
import abc
from pprint import pprint
import importlib

from loguru import logger
from RssParser.schema import SubscribeWebsite, UpdateRecord, Entity, Database
import RssParser.config as config


class Parser:
    link: str
    xml: str
    entity: dict

    def __init__(self, link) -> None:
        self.link = link

    def client(self):
        transport = httpx.AsyncHTTPTransport(retries=4)
        return httpx.AsyncClient(proxy=config.proxy, transport=transport)

    async def get(self):
        async with self.client() as client:
            retries = 0
            while True:
                try:
                    retries += 1
                    logger.info(f"try to get: {self.link}...")
                    res = await client.get(self.link)
                    logger.info(f"get {self.link} success")
                    break
                except httpx.ReadTimeout:
                    logger.warning(f"get {self.link} timeout, retry: {retries}/{3} ...")
                    if retries > 3:
                        logger.error(f"get {self.link} Timeout")
                        raise httpx.ReadTimeout
            self.xml = res.text

    def html_parser(self):
        logger.info("parse xml")
        self.entity = feedparser.parse(self.xml)
        logger.info("parser done")

    async def parser(self):
        await self.get()
        self.html_parser()
        return self.entity


class Crawler:
    def __init__(self) -> None:
        self.database = Database()
        self.crawler_modules = importlib.import_module('RssParser.rss_entity')
        self.crawler_list = [x for x in dir(self.crawler_modules) if isclass(getattr(self.crawler_modules, x))]  # all implement class in model
        self.check_constructor()

    def check_constructor(self):
        name_list = [item.name for item in self.database.get_subscribe()]
        for i in name_list:
            if i not in self.crawler_list:
                raise Exception(f'Construct Entity: <{i}> is not implement, please define entity in "rss_entity.py".')

    def construct_entity(self, entity_type, xml_entity: dict) -> Entity:
        return getattr(self.crawler_modules, entity_type)(xml_entity).get_entity()

    async def get_subscribe(self):
        li = []
        for rss in self.database.get_subscribe():
            li.append({
                'id': rss.id,
                'entity': rss,
                'parser': Parser(rss.url),
            })

        await asyncio.gather(*[i['parser'].parser() for i in li])
        return li

    def update_record(self, website_id):
        record = UpdateRecord(website_id=website_id, update_time=datetime.datetime.now())
        self.database.session.add(record)
        self.database.session.commit()

    async def update_subscribe(self):
        items = await self.get_subscribe()
        for website in items:
            sql_entities = []
            for i in website['parser'].entity.entries:
                if self.database.session.get(Entity, i['title']) is None:  # was existed, pass
                    sql_entities.append(self.construct_entity(website['entity'].name, i))
            # self.database.session.add_all(sql_entities)  # 每一个组的对象加入数据库
            for i in sql_entities:
                self.database.session.merge(i)
            self.database.session.add(
                UpdateRecord(website_id=website['id'], update_time=datetime.datetime.now()))  # 更新完一个组(RSS网站)后记录已经更新过的信息
            self.database.session.commit()
            logger.info(f'update {website} success')
        logger.info("update all done")

# par1 = Parser('https://nyaa.si/?page=rss')
# par2 = Parser('https://share.acgnx.se/rss.xml')

# if __name__ == "__main__":
#     db = Database()
#     for i in db.get_subscribe():
#         print(i)
#     db.delete_subscribe(2)
#     db.add_subscribe('nyaa', 'https://nyaa.si/?page=rss')
#     db.add_subscribe('acgnx', 'https://share.acgnx.se/rss.xml')
if __name__ == "__main__":
    pass