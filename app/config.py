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

        database_url = env.str("DATABASE_URL", "sqlite:///app.db")
        secret_key = env.str("SECRET_KEY", "dev-secret-key-change-in-production")
        debug = env.bool("DEBUG", False)

        logger.info(f"DATABASE_URL: {database_url}")
        logger.info(f"SECRET_KEY: {secret_key}")
        logger.info(f"DEBUG: {debug}")

        config = Config(
            db=DataBaseConfig(database_url=database_url),
            secret_key=secret_key,
            debug=debug,
        )
        logger.info(f"Конфигурация загружена: {config}")
        return config
    except Exception as e:
        logger.error(f"Ошибка загрузки конфигурации: {e}")
        raise
