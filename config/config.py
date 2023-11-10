from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_URI: str
    MONGO_DATABASE_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_AUTH_DATABASE: int
    REDIS_TOKEN_DATABASE: int

    ACCESS_TOKEN_LIFETIME: int
    REFRESH_TOKEN_LIFETIME: int
    SECRET_KEY: str
    ALGORITHM: str

    NOTIFICATION_REGISTER_URL: str
    NOTIFICATION_RESET_PASSWORD_URL: str

    ELASTICSEARCH_HOST: str
    ELASTICSEARCH_PORT: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache
def load_settings():
    return Settings()


settings = load_settings()
