# Python
from fastapi import FastAPI

from .config import load_config
from .logger import logger
from .models import User


app = FastAPI()

user = User(name="John Doe", id=1)


@app.get("/")
# Python
@app.get("/")
def read_root():
    try:
        print("Начало выполнения read_root")
        config = load_config()
        print(f"Конфигурация загружена: {config}")
        logger.debug("Тестовое сообщение для проверки логгера")
        logger.info(f"Connected to database: {config.db.database_url}")
        return {"database_url": config.db.database_url}
    except Exception as e:
        print(f"Ошибка: {e}")
        logger.error(f"Error connecting to database: {e}")
        return {"error": "Failed to connect to database"}


@app.get("/custom")
def read_custom_message():
    return {"message": "This is a custom message!!!"}


@app.get("/users")
def create_user(user: User):
    return user
