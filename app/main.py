# Python
from fastapi import FastAPI

from .config import load_config
from .logger import logger
from .models import User


app = FastAPI()

class UsersAge(User):
    is_adult: bool = True

    def __init__(self, name: str, age: int, **kwargs):
        super().__init__(name=name, age=age, **kwargs)
        self.is_adult = age >= 18

user = UsersAge(name = "John Doe", age = 17)


@app.get("/")
# Python
@app.get("/")
def read_root():
    try:
        logger.info("Начало выполнения read_root")
        config = load_config()
        logger.info(f"Конфигурация загружена: {config}")
        logger.info(f"Connected to database: {config.db.database_url}")
        return {"database_url": config.db.database_url}
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        logger.error(f"Error connecting to database: {e}")
        return {"error": "Failed to connect to database"}


@app.get("/custom")
def read_custom_message():
    return {"message": "This is a custom message!!!"}


@app.get("/users")
def get_user():
    # return {"name": user.name, "id": user.id}
    return user.__dict__

