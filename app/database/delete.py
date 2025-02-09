import os
import sqlite3

DB_PATH = os.path.abspath("app/database/news.db")  # Абсолютный путь


def delete_news_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS news;")  # Удаление таблицы, если она существует

    conn.commit()
    conn.close()
    print("Таблица news удалена.")

delete_news_table()