from dataclasses import dataclass
from typing import Optional

from environs import Env

from .logger import logger


@dataclass
class DataBaseConfig:
    database_url: str


@dataclass
class Config:
    db: DataBaseConfig
    secret_key: str
    debug: bool = False

# Python
def load_config(path: Optional[str] = None) -> Config:
    env = Env()
    try:
        logger.info("Начало загрузки конфигурации...")
        if path:
            logger.info(f"Чтение .env файла по указанному пути: {path}")
            env.read_env(path)
        else:
            logger.info("Чтение .env файла из корня проекта")
            env.read_env()
        logger.info("Файл .env загружен успешно")
        logger.info(f"DATABASE_URL: {env.str('DATABASE_URL', 'sqlite:///app.db')}")
        logger.info(f"SECRET_KEY: {env.str('SECRET_KEY', 'dev-secret-key-change-in-production')}")
        logger.info(f"DEBUG: {env.bool('DEBUG', False)}")
        config = Config(
            db=DataBaseConfig(database_url=env.str("DATABASE_URL", "sqlite:///app.db")),
            secret_key=env.str("SECRET_KEY", "dev-secret-key-change-in-production"),
            debug=env.bool("DEBUG", False),
        )
        logger.info(f"Конфигурация загружена: {config}")
        return config
    except Exception as e:
        logger.error(f"Ошибка загрузки конфигурации: {e}")
        raise
