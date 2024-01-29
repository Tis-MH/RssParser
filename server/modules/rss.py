import datetime

from pydantic import BaseModel

class Rss(BaseModel):
    id: int
    name: str
    url: str
    interval: int | None = None
    update: bool
    
class UpdateRecord(BaseModel):
    id: int
    website_id: int
    update_time: datetime.datetime
    
class Entity(BaseModel):
    title: str
    magnet: str
    update_time: datetime.datetime | None = None
    category: str | None = None
    size: str | None = None