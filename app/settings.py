from pydantic_settings import BaseSettings
from functools import lru_cache

import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Settings(BaseSettings):
    title: str = "TITLE"
    version: str = "VERSION"
    description: str = "DESCRIPTION"
    host: str = "DB_HOST"
    port: str = "DB_PORT"
    name: str = "DB_NAME"
    user: str = "DB_USER"
    passw: str = "DB_PASS"
    db_url: str = "DATABASE_URL"
    # class Config:
    #     env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
