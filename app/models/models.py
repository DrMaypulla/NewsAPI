from pydantic import BaseModel

class NewsItem(BaseModel):
    title: str
    description: str
    content: str
    image_id: str
