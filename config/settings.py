# 임포트 섹션
import datetime
import os
import pymysql

# MySQL DB를 위한 설정
pymysql.install_as_MySQLdb()

# 기본 디렉토리 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR_BACKEND = BASE_DIR

# 정적 파일 설정
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# 보안 설정
SECRET_KEY = 'django-insecure-=e!g&p-3@smi7j^=@hx06v)=m^w$5q6@+1nbl@@n%fg$53wf#e'
DEBUG = True
ALLOWED_HOSTS = []
PORT = 8001  # Change to a different port
SWAGGER_SETTINGS = {
    'DEFAULT_AUTO_SCHEMA_CLASS': 'drf_yasg.inspectors.SwaggerAutoSchema',
}

BATON = {
    "SITE_HEADER": "TWEAK BACK OFFICE",
    "SITE_TITLE": "TWEAK BACK OFFICE",
    "INDEX_TITLE": "관리 페이지",
    # "SUPPORT_HREF": "https://juice.co.kr/",
    "SUPPORT_HREF": "mailto:tweaker.202306@gmail.com",
    "COPYRIGHT": "copyright © WheelCompany All Rights Reserved.",
    "POWERED_BY": '<a href="https://tweak-english.com/">TWEAK</a>',
    'CONFIRM_UNSAVED_CHANGES': True,
    'SHOW_MULTIPART_UPLOADING': True,
    'ENABLE_IMAGES_PREVIEW': True,
    'CHANGELIST_FILTERS_IN_MODAL': True,
    'CHANGELIST_FILTERS_ALWAYS_OPEN': False,
    'CHANGELIST_FILTERS_FORM': True,
    'MENU_ALWAYS_COLLAPSED': False,
    'MENU_TITLE': 'Menu',
    'MESSAGES_TOASTS': False,
    'GRAVATAR_DEFAULT_IMG': 'retro',
    'GRAVATAR_ENABLED': True,
    'LOGIN_SPLASH': '/static/core/img/login-splash.png',
    'FORCE_THEME': None,
    'SEARCH_FIELD': {
        'label': 'Label shown as placeholder',
        'url': '/api/',
    },
    'MENU': (
        { 'type': 'title', 'label': 'main', 'apps': ('auth', ) },
        {
            'type': 'app',
            'name': 'auth',
            'label': 'Authentication',
            'icon': 'fa fa-lock',
            'models': (
                {
                    'name': 'user',
                    'label': 'Users'
                },
                {
                    'name': 'group',
                    'label': 'Groups'
                },
            )
        },
        { 'type': 'title', 'label': 'Contents', 'apps': ('flatpages', ) },
        { 'type': 'model', 'label': 'Pages', 'name': 'flatpage', 'app': 'flatpages' },
        { 'type': 'free', 'label': 'Custom Link', 'url': 'http://www.google.it', 'perms': ('flatpages.add_flatpage', 'auth.change_user') },
        { 'type': 'free', 'label': 'My parent voice', 'default_open': True, 'children': [
            { 'type': 'model', 'label': 'A Model', 'name': 'mymodelname', 'app': 'myapp' },
            { 'type': 'free', 'label': 'Another custom link', 'url': 'http://www.google.it' },
        ] },
    ),
    # 'ANALYTICS': {
    #     'CREDENTIALS': os.path.join(BASE_DIR, 'credentials.json'),
    #     'VIEW_ID': '12345678',
    # }
}

# 설치된 앱 목록
INSTALLED_APPS = [
    # admin 테마
    'baton',
    # Django 기본 앱
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 커스텀 앱
    'api',
    # 서드파티 앱
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'drf_yasg', #drf_yasg
    'baton.autodiscover',
]

# 미들웨어 설정
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'config.middleware.CustomResponseMiddleware'
]

# URL 설정
ROOT_URLCONF = 'config.urls'

# 템플릿 설정
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI 앱 설정
WSGI_APPLICATION = 'config.dev.wsgi.application'

# 데이터베이스 설정
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

# 패스워드 유효성 검사 설정
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 국제화 설정
LANGUAGE_CODE = 'ko'
TIME_ZONE = 'Asia/Seoul'

# REST 프레임워크 설정
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": (
        # "rest_framework.authentication.BasicAuthentication",
        # "rest_framework.authentication.SessionAuthentication",
        "rest_framework.permissions.IsAuthenticated",
        "rest_framework.permissions.AllowAny",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
}

# JWT 설정
JWT_AUTH = {
    "JWT_EXPIRATION_DELTA": datetime.timedelta(days=2),
    "JWT_ALLOW_REFRESH": True,
    "JWT_REFRESH_EXPIRATION_DELTA": datetime.timedelta(days=7),
    "JWT_AUTH_HEADER_PREFIX": "JWT",
}

# CORS 설정
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_CREDENTIALS = True
