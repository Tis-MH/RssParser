from datetime import datetime
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    create_engine,
    Boolean,
)
import hashlib
import requests
from os import path
from loguru import logger


logger.add("log/file_2.log", rotation="10 MB", level="INFO")

from sqlalchemy.orm import declarative_base, Session, relationship

engine = create_engine("sqlite:///sqlite.sql")

session = Session(engine)

Base = declarative_base()


class SubscribeWebsite(Base):
    __tablename__ = "subscribe_website"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False, unique=True)
    enable = Column(Boolean(), nullable=False)


class SubscribeRecord(Base):
    __tablename__ = "subscribe_record"
    id = Column(String(255), primary_key=True)
    update_time = Column(DateTime, nullable=False)
    website_id = Column(Integer, ForeignKey("subscribe_website.id"), nullable=False)

    website = relationship(
        "SubscribeWebsite", foreign_keys=[website_id], backref="records"
    )


def download_rss(url: str, save_path="./result", max_retries=3):
    retries = 0

    def request(url: str):
        nonlocal retries
        try:
            response = requests.get(url, timeout=10)
            logger.info(f"success download {url}")
            return response
        except requests.Timeout:
            retries += 1
            logger.warning(f"retry to connect: {url}... {retries}/{max_retries}")
            if retries > max_retries:
                logger.error(f"connect to {url} timeout, retries: {max_retries}")
                raise requests.Timeout
            return request(url)

    html = request(url).text
    file_hash = hashlib.sha1(html.encode("utf-8")).hexdigest()
    with open(path.join(save_path, file_hash + ".xml"), "w", encoding="utf-8") as f:
        f.write(html)
    return file_hash


def download_all():
    websites = session.query(SubscribeWebsite).where(SubscribeWebsite.enable == True)
    for website in websites:
        try:
            file_hash = download_rss(website.url)
            record = SubscribeRecord(
                id=file_hash, update_time=datetime.now(), website_id=website.id
            )
            session.add(record)
            session.commit()
        except Exception as e:
            logger.error(f"download {website.url} raise a error: {str(e)}")

def add_subscribe():
    subscibes = [SubscribeWebsite(
        name="dmhy", url="https://dmhy.org/topics/rss/rss.xml", enable=True
    ),
    SubscribeWebsite(
        name="mori", url="https://share.acgnx.se/rss.xml", enable=True
    )]
    session.add_all(subscibes)
    session.commit()


Base.metadata.create_all(engine)
# session.add(website)
# session.commit()

#add_subscribe()
download_all()
# download_rss("https://dmhy.org/topics/rss/rss.xml")
