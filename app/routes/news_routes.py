from fastapi import APIRouter, Query, UploadFile, File, HTTPException, FastAPI
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # `app/`
UPLOAD_DIR = os.path.join(BASE_DIR, "static")  # `app/static/`
DB_PATH = os.path.join(BASE_DIR,"database", "news.db")  # Путь к БД

news = APIRouter()

@news.post("/news/create", tags=["news"])
async def create_news(
    title: str = Query(..., alias="title"),
    description: str = Query(..., alias="description"),
    content: str = Query(..., alias="content"),
    image: UploadFile = File(...)
):
    try:

        image_path = os.path.join(UPLOAD_DIR, image.filename)
        relative_image_path = f"static/{image.filename}"
        with open(image_path, "wb") as buffer:
            buffer.write(await image.read())

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO news (title, description, content, image_url)
            VALUES (?, ?, ?, ?)
        """, ( title, description, content, relative_image_path))
        news_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return {
            "id": news_id,
            "title": title,
            "description": description,
            "content": content,
            "image_url": relative_image_path
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating news: {str(e)}")
@news.get("/news/all", tags=["news"])
async def get_all_news():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM news")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    conn.close()
    news_list = [dict(zip(column_names, row)) for row in rows]

    return news_list


@news.delete("/news/delete/{id}", tags=["news"])
async def delete_news(id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM news WHERE id = ?", (id,))
    news_item = cursor.fetchone()
    if not news_item:
        conn.close()
        raise HTTPException(status_code=404, detail="Новость не найдена")
    cursor.execute("DELETE FROM news WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return {"message": "Новость успешно удалена", "id": id}
