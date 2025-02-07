from fastapi import APIRouter, Query, UploadFile, File, HTTPException, FastAPI
from fastapi.responses import StreamingResponse
import app.database.mongo
from bson.objectid import ObjectId

news = FastAPI()
collection = app.database.mongo.db["news"]


@news.post("/news/create")
async def create_news(
        title: str = Query(..., alias="title"),
        description: str = Query(..., alias="description"),
        content: str = Query(..., alias="content"),
        image: UploadFile = File(...)
):
    # Чтение данных изображен
    image_id = await app.database.mongo.fs.upload_from_stream(image.filename, image.file)

    # Формируем документ для базы данных
    news_dict = {
        "_id": (ObjectId()),  # Генерация нового ID для записи
        "title": title,
        "description": description,
        "content": content,
        "image_id": image_id,
    }

    # Вставляем документ в MongoDB (асинхронно)
    await collection.insert_one(news_dict)

    news_dict["_id"] = str(news_dict["_id"])
    news_dict["image_id"] = str(news_dict["image_id"])

    return {"message": image}

"""@news.post("/create")
async def create_news(news_item: NewsItem):
    news = {"_id": str(ObjectId()), **news_item.dict()}
    # Возвращаем результат
    return news"""


@news.get("/news/all")
async def get_all_news():
    cursor = collection.find({})
    news_list = []

    async for news_item in cursor:
        # Convert ObjectId to string for all fields
        news_item["_id"] = str(news_item["_id"])
        news_item["image_id"] = str(news_item["image_id"])

        # Append the document to the list
        news_list.append(news_item)

    return news_list

@news.delete("/news/delete/{id}")
async def delete_news(id: str):
    if not ObjectId.is_valid(id):  # Проверка на правильность формата ObjectId
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    delete_filter = {"_id": ObjectId(id)}
    result = await collection.find_one_and_delete(delete_filter)
    if not result:
        raise HTTPException(status_code=404, detail="Новость не найдена")
    return {"message": "Новость успешно удалена", "id": id}


@news.get("/news/download/{id}")
async def download_news_image(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")

    object_id = ObjectId(id)

    try:
        # Open the download stream for the file
        file_stream = await app.database.mongo.fs.open_download_stream(object_id)

        # Return the file as a streaming response
        return StreamingResponse(file_stream, media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={file_stream.filename}"})
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"File not found: {str(e)}")