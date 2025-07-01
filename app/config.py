from dataclasses import dataclass
from typing import Optional

from environs import Env


@dataclass
class DataBaseConfig:
    database_url: str


@dataclass
class Config:
    db: DataBaseConfig
    secret_key: str
    debug: bool = False


# Python
# Python
def load_config(path: Optional[str] = None) -> Config:
    env = Env()
    try:
        print("Начало загрузки конфигурации...")
        if path:
            print(f"Чтение .env файла по указанному пути: {path}")
            env.read_env(path)
        else:
            print("Чтение .env файла из корня проекта")
            env.read_env()
        print("Файл .env загружен успешно")
        print(f"DATABASE_URL: {env.str('DATABASE_URL', 'sqlite:///app.db')}")
        print(f"SECRET_KEY: {env.str('SECRET_KEY', 'dev-secret-key-change-in-production')}")
        print(f"DEBUG: {env.bool('DEBUG', False)}")
        config = Config(
            db=DataBaseConfig(database_url=env.str("DATABASE_URL", "sqlite:///app.db")),
            secret_key=env.str("SECRET_KEY", "dev-secret-key-change-in-production"),
            debug=env.bool("DEBUG", False),
        )
        print(f"Конфигурация загружена: {config}")
        return config
    except Exception as e:
        print(f"Ошибка загрузки конфигурации: {e}")
        raise
