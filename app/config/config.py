from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

load_dotenv()  # Загрузка переменных окружения из .env файла


class Settings(BaseSettings):
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = int(os.getenv("DB_PORT"))
    DB_USER: str = os.getenv("DB_USER")
    DB_PASS: str = os.getenv("DB_PASS")
    DB_NAME: str = os.getenv("DB_NAME")

    PRIVATE_KEY_PATH: str = os.getenv("PRIVATE_KEY_PATH")
    PUBLIC_KEY_PATH: str = os.getenv("PUBLIC_KEY_PATH")
    ALGORITHM: str = "RS256"
    access_token_expire_minutes: int = 10
    refresh_token_expire_days: int = 7

    @property
    def ACCESS_TOKEN_EXPIRE_MINUTES(self):
        return self.access_token_expire_minutes

    @property
    def REFRESH_TOKEN_EXPIRE_DAYS(self):
        return self.refresh_token_expire_days

    @property
    def PRIVATE_KEY(self):
        with open(self.PRIVATE_KEY_PATH, "r") as file:
            private_key = file.read()
        return private_key

    @property
    def PUBLIC_KEY(self):
        with open(self.PUBLIC_KEY_PATH, "r") as file:
            public_key = file.read()
        return public_key

    @property
    def ALGORITHM_TYPE(self):
        return f"{self.ALGORITHM}"

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def ECHO_STATUS_ON(self):
        return True

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
