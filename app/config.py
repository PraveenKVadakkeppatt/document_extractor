import os
from dotenv import load_dotenv


load_dotenv()


class Settings:

    DB_SERVER = os.getenv("DB_SERVER")
    DB_NAME = os.getenv("DB_NAME")
    DB_DRIVER = os.getenv("DB_DRIVER")

    DOCUMENT_STORAGE = r"D:\document_storage"

settings = Settings()
