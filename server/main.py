from typing import Union

from fastapi import FastAPI
import uvicorn
from uvicorn import run

from router.rss import router

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    run('main:app', reload=True)
