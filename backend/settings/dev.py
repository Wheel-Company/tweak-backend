from backend.settings.base import *

DEBUG = True
# CORS 관련

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "tweak",
        "USER": "root",
        "PASSWORD": "tweak500!",
        "HOST": "127.0.0.1",  # Or an IP Address that your DB is hosted on
        # "HOST": "easyear01-test.c9yoxqhzjvtb.ap-northeast-2.rds.amazonaws.com",
        "PORT": "3306",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


# WSGI_APPLICATION = "backend.development.wsgi.application"

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

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {
#         "file": {
#             "level": "ERROR",
#             "class": "logging.FileHandler",
#             "filename": os.path.join(BASE_DIR_BACKEND, "logs") + "/log.txt",
#         },
#     },
#     "loggers": {
#         "django": {
#             "handlers": ["file"],
#             "level": "ERROR",
#             "propagate": True,
#         },
#     },
# }
