from functools import lru_cache
from pydantic import BaseSettings
from pathlib import Path

IMAGES_DIR = 'fastapi_blog/images'
BASE_DIR = Path(__file__).resolve().parent.parent.joinpath(IMAGES_DIR)
ARTICLES_IMAGE_DIR = BASE_DIR / 'articles'


class Settings(BaseSettings):
    test_database_url: str
    secret_key: str

    # algorithm for jwt
    algorithm: str
    access_token_expire_minutes: int

    # database settings
    postgres_user: str
    postgres_password: str
    postgres_db_name: str
    postgres_server: str
    postgres_port: int

    articles_image_url: str
    test_image_path: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache
def get_settings() -> Settings:
    return Settings()
