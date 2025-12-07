from .settings import *

DEBUG = True
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_Path = BASE_DIR.parent.parent / ".env"
load_dotenv(dotenv_path=ENV_Path)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



LOG_DIR = BASE_DIR / "logs"
os.makedirs(LOG_DIR, exist_ok=True)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s %(pathname)s %(lineno)d',
        },
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': LOG_DIR / 'app.log',
            'formatter': 'json',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'api': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# import dj_database_url

# DATABASES = {
#     "default": dj_database_url.parse(
#         os.environ.get("DATABASE_URL", "postgres://postgres:postgres@db:5432/book_exchange_db")
#     )
# }


tmpPostgres = urlparse(os.getenv("DATABASE_URL"))
# print(BASE_DIR.parent.parent.parent)
port = os.getenv("DB_PORT")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': tmpPostgres.path.replace('/', ''),
        'USER': tmpPostgres.username,
        'PASSWORD': tmpPostgres.password,
        'HOST': tmpPostgres.hostname,
        'PORT': port,
        'OPTIONS': dict(parse_qsl(tmpPostgres.query)),
    }
}