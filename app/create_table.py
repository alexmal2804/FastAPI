import sqlite3

DB_NAME = "database.sqlite"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Создание таблицы items: id, name
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
"""
)

conn.commit()
conn.close()  # Закрытие соединения с базой данных
