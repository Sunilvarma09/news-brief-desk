from pydantic import BaseModel
from datetime import datetime

class NewsItem(BaseModel):
    id:str
    title: str
    content: str
    source:str
    published_at:datetime
    received_at:datetime

class Story(BaseModel):
    story_id:str
    brief:str  
    news_items:list[NewsItem]
    status:str
    created_at:datetime
    published_at: datetime | None = None
