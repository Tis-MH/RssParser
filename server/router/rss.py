from typing import List
from fastapi import APIRouter, Depends, HTTPException
from RssParser import schema
from server.modules.base import TResult
from server.modules.rss import Rss
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
    items = [item.model_dump() for item in database.get_subscribe()]
    return {
        'code': 200,
        'res': items
    }
        


# @router.get("/{item_id}")
# async def read_item(item_id: str):
#     if item_id not in fake_items_db:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return {"name": fake_items_db[item_id]["name"], "item_id": item_id}


@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}