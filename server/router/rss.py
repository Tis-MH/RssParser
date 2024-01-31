from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from RssParser import schema
from server.modules.base import TResult
from server.modules.rss import Rss
from sqlalchemy.exc import NoResultFound
# from ..dependencies import get_token_header

router = APIRouter(
    prefix="/rss",
    tags=["rss"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

database = schema.Database()


@router.get("/", response_model=TResult[List[Rss]])
async def read_items():
    # items = [item.model_dump() for item in database.get_subscribe()]
    execution = select(schema.SubscribeWebsite).where(schema.SubscribeWebsite.update == True)
    items = [item.model_dump() for item in database.session.exec(execution)]
    return {
        'code': 200,
        'res': items
    }
   
@router.patch("/", response_model=TResult[str])
async def change_status(subscribe_id: int, status: bool):
    try:
        entity = database.session.get_one(schema.SubscribeWebsite, subscribe_id)
    except NoResultFound:
        return {
            'code': 50001,
            'res': 'not found'
        }
    entity.update = status
    database.session.add(entity)
    database.session.commit()
    return {
        'code': 200,
        'res': 'success'
    }

@router.post("/", response_model=TResult[int])
async def create_subscribe(name: str, url: str, interval: int | None = None, update: bool = True):
    entity = schema.SubscribeWebsite(name=name, url=url, interval=interval, update=update)
    database.session.add(entity)
    database.session.commit()
    return {
        'code': 200,
        'res': entity.id
    }

@router.delete("/", response_model=TResult[str])
async def delete_subscribe(subscribe_id: int):
    try:
        entity = database.session.get_one(schema.SubscribeWebsite, subscribe_id)
    except NoResultFound:
        return {
            'code': 50001,
            'res': 'not found'
        }
    database.session.delete(entity)
    database.session.commit()
    return {
        'code': 200,
        'res': 'success'
    }