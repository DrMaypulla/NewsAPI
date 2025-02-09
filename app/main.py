from fastapi import  FastAPI
import routes.news_routes
from fastapi.staticfiles import StaticFiles
import os
app = FastAPI()

news = routes.news_routes.news
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Получаем путь к `main.py`
STATIC_DIR = os.path.join(BASE_DIR, "static")  # Теперь это `app/static/`

# Раздаем файлы из `static/`
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(news)