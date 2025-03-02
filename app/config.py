from dotenv import load_dotenv
import os

# Загружаем переменные окружения из .env файла
load_dotenv()

class Settings():
    DATABASE_HOST: str = os.getenv("DATABASE_HOST")
    DATABASE_PORT: str = os.getenv("DATABASE_PORT")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME")
    DATABASE_USER: str = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD")

    class Config:
        env_file = ".env"

settings = Settings()