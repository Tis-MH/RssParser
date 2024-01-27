import asyncio
import importlib
import unittest
import os
from loguru import logger
import sys

sys.path.append(f'{os.getcwd()}')
# os.chdir('../')

from rss_parser import Crawler, Database


class TestDataBase(unittest.TestCase):
    def setUp(self) -> None:
        logger.add("log/TestDataBase_{time}.log")

        if 'sqlite3.sql' in os.listdir():
            os.remove('sqlite3.sql')
        return super().setUp()

    def test_database_manipulate(self):
        db = Database()
        db.add_subscribe('nyaa', 'https://nyaa.si/?page=rss')
        db.add_subscribe('acgnx', 'https://share.acgnx.se/rss.xml')
        db.add_subscribe('123', '123')
        db.delete_subscribe(3)
        for i in db.get_subscribe():
            print(i)


class TestCrawler(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        logger.add("log/TestCrawler_{time}.log")
        self.db = Database()
        self.crawler = Crawler()
        return super().setUp()

    def test_crawler(self):
        res = asyncio.run(self.crawler.get_subscribe())
        logger.info(res)

    def test_crawler_and_record(self):
        res = asyncio.run(self.crawler.update_subscribe())
        logger.info(res)

    async def test_subscribe_grps(self):
        import itertools
        items = await self.crawler.get_subscribe()
        for website in items:
            sql_entities = [self.crawler.construct_entity(website['entity'].name, item) for item in
                            website['parser'].entity.entries]
            logger.info(sql_entities)

    async def test_update_subscribe(self):
        await self.crawler.update_subscribe()
