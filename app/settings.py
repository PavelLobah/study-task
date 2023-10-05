from pydantic import BaseModel
from functools import lru_cache

import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Settings(BaseModel):
    title: str = os.getenv("TITLE")
    version: str = os.getenv("VERSION")
    description: str = os.getenv("DESCRIPTION")

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
