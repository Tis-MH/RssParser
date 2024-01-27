import asyncio
import rss_parser
from time import sleep

async def main():
    crawler = rss_parser.Crawler()
    await crawler.update_subscribe()

if __name__ == "__main__":
    while True:
        asyncio.run(main)
        sleep(1440)