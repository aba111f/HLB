from .settings import *

DEBUG = True
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_Path = BASE_DIR.parent / ".env"


import dj_database_url

DATABASES = {
    "default": dj_database_url.parse(
        os.environ.get("DATABASE_URL", "postgres://postgres:postgres@db:5432/book_exchange_db")
    )
}