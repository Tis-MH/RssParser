import asyncio
import unittest
import os
from loguru import logger
import sys
import httpx
import json

sys.path.append(f'{os.getcwd()}')

class TestBackend(unittest.IsolatedAsyncioTestCase):
    async def test_create_subscribe(self):
        async with httpx.AsyncClient() as client:
            response = await client.get('http://127.0.0.1:8000/rss/')
            print(response.text)
    
    async def test_delete_subscribe(self):
        async with httpx.AsyncClient() as client:
            response = await client.delete('http://127.0.0.1:8000/rss/')
            print(response.text)
    
    async def test_get_subscribe(self):
        pass
    
    async def test_update_subscribe(self):
        async with httpx.AsyncClient() as client:
            response = await client.patch('http://127.0.0.1:8000/rss/?subscribe_id=1&status=true')
            js = json.loads(response.text)
            print(js)