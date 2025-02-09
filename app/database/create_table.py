import sqlite3
import os

DB_PATH = "app/database/news.db"

# Создаём директорию, если её нет
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Подключаемся к БД (если её нет, она создастся)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Создаём таблицу, если её нет
cursor.execute("""
    CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        content TEXT NOT NULL,
        image_url TEXT
    )
""")
conn.commit()
conn.close()

print(f"База данных создана: {DB_PATH}")