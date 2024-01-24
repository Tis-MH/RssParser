import asyncio
import unittest
import os
from loguru import logger
import sys

sys.path.append(f'{os.getcwd()}')

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
            
class TestCrawler(unittest.TestCase):
    def setUp(self) -> None:
        logger.add("log/TestCrawler_{time}.log")
        self.db = Database()
        self.crawler = Crawler()
        return super().setUp()
    
    def test_crawler(self):
        res = asyncio.run(self.crawler.update_subscribe())
        logger.info(res)

