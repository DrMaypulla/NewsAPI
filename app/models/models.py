from pydantic import BaseModel
from typing import Optional


class NewsItem(BaseModel):
    title: str
    description: str
    content: str
    image_id: str
