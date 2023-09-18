import logging
from pickle import TRUE
from config.settings import *

DEBUG = True
# CORS 관련

ALLOWED_HOSTS =['*']
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "tweak",
        "USER": "wheelcompany",
        "PASSWORD": "Wheel202307!",
        "HOST": "tweak.cawqlcmytbf3.ap-northeast-2.rds.amazonaws.com",  # Or an IP Address that your DB is hosted on
        # "HOST": "easyear01-test.c9yoxqhzjvtb.ap-northeast-2.rds.amazonaws.com",
        "PORT": "3306",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = [
    "http://127.0.0.1:3001",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CSRF_TRUSTED_ORIGINS = (
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
)

LOG_LEVEL = 'INFO'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': u'[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s'
        },
    },
    'handlers': {
        'file_handler': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'my-logging.log'),
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 10,
            'formatter': 'default',
        },
        'stream_handler': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'mail_admins' : {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        'stream_logger': {
            'handlers': ['file_handler'],
            'level': LOG_LEVEL,
            'propagate': False
        },
        'file_logger': {
            'handlers': ['stream_handler']
        },
        'celery_heartbeat': {
            'handlers': ['stream_handler'],#['mail_admins'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
    }
}
