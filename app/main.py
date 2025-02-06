from fastapi import FastAPI, Query, UploadFile, File, HTTPException
from database import db, fs
from bson.objectid import ObjectId

news = FastAPI()
collection = db["news"]


@news.post("news/create")
async def create_news(
        title: str = Query(..., alias="title"),
        description: str = Query(..., alias="description"),
        content: str = Query(..., alias="content"),
        image: UploadFile = File(...)
):
    # Чтение данных изображения
    image_data = await image.read()  # Чтение данных файла

    # Загружаем изображение в GridFS
    image_id = await fs.upload_from_stream(image.filename, image.file)

    # Формируем документ для базы данных
    news_dict = {
        "_id": (ObjectId()),  # Генерация нового ID для записи
        "title": title,
        "description": description,
        "content": content,
        "image_id": image_id,  # Сохраняем ID изображения из GridFS как строку
    }

    # Вставляем документ в MongoDB (асинхронно)
    await collection.insert_one(news_dict)

    news_dict["_id"] = str(news_dict["_id"])
    news_dict["image_id"] = str(news_dict["image_id"])
    return news_dict

"""@news.post("/create")
async def create_news(news_item: NewsItem):
    news = {"_id": str(ObjectId()), **news_item.dict()}
    # Возвращаем результат
    return news"""


@news.get("news/all")
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

@news.delete("news/delete/{id}")
async def delete_news(id: str):
    if not ObjectId.is_valid(id):  # Проверка на правильность формата ObjectId
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    delete_filter = {"_id": ObjectId(id)}
    result = await collection.find_one_and_delete(delete_filter)
    if not result:
        raise HTTPException(status_code=404, detail="Новость не найдена")
    return {"message": "Новость успешно удалена", "id": id}

