from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_URI: str
    MONGO_DATABASE_NAME: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DATABASE_NUMBER: int
    ACCESS_TOKEN_LIFETIME: int
    REFRESH_TOKEN_LIFETIME: int
    SECRET_KEY: str
    ALGORITHM: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
