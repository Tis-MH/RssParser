import asyncio
from RssParser import rss_parser
from time import sleep
import config
from loguru import logger

logger.add("log/file_1.log", rotation="10 MB", level="info")


async def main():
    crawler = rss_parser.Crawler()
    await crawler.update_subscribe()


if __name__ == "__main__":
    while True:
        asyncio.run(main())
        sleep(config.interval)
