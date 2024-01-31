from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from RssParser import schema
from server.modules.base import TResult
from server.modules.rss import Rss
from sqlalchemy.exc import NoResultFound

router = APIRouter(
    prefix="/rss",
    tags=["rss"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

database = schema.Database()

