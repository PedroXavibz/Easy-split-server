from dotenv import load_dotenv
from uvicorn.config import os

load_dotenv()


class Config:
    HOST = os.getenv(key='LOCALHOST', default='localhost')
    PORT = int(os.getenv(key='PORT', default=5000))
    DEBUG = bool(os.getenv(key='DEBUG', default=True))
    RELOAD = bool(os.getenv(key='RELOAD', default=True))
    LOG_LEVEL = os.getenv(key='LOG_LEVEL', default='info')

    DB_URL = os.getenv(key='DB_URL', default='')
    DB_NAME = os.getenv(key='DB_NAME', default='')
