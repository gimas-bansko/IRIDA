"""
Общи настройки за всички обкръжения.

Този файл НЕ съдържа тайни и НЕ решава дали DEBUG е включен - това е работа
на dev.py / prod.py. Всичко чувствително се чете от обкръжението (.env).

Избор на обкръжение:
    DJANGO_SETTINGS_MODULE=config.settings.dev   (по подразбиране в manage.py)
    DJANGO_SETTINGS_MODULE=config.settings.prod
"""

from pathlib import Path

import environ

# BASE_DIR = директорията на Django проекта (там са manage.py, templates/, frontend/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# REPO_ROOT = коренът на хранилището (там са .env, requirements/)
REPO_ROOT = BASE_DIR.parent

env = environ.Env()

# .env се търси първо до manage.py, после в корена на хранилището.
for _candidate in (BASE_DIR / '.env', REPO_ROOT / '.env'):
    if _candidate.exists():
        env.read_env(_candidate)
        break


# ***************************************
#              Приложения
# ***************************************
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
]

LOCAL_APPS = [
    'main',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'


# ***************************************
#               Шаблони
# ***************************************
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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


# ***************************************
#             База данни
# ***************************************
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME', default='irida'),
        'USER': env('DB_USER', default='irida'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='3306'),
        'OPTIONS': {'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ***************************************
#          Аутентикация
# ***************************************
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'subject_list'  # ползва се от Django auth views, но и ние го спазваме в redirect
LOGOUT_REDIRECT_URL = 'login'


# ***************************************
#          REST framework
# ***************************************
# По подразбиране DRF ползва AllowAny. Тук обръщаме презумпцията:
# всеки endpoint иска логнат потребител, освен ако изрично не каже друго.
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
}


# ***************************************
#        Език, време, локализация
# ***************************************
LANGUAGE_CODE = 'bg'

TIME_ZONE = 'Europe/Sofia'
TIME_FORMAT = 'H:i'  # 24-часов формат
DATETIME_FORMAT = 'Y-m-d H:i:s'  # 2024-12-25 14:30:00

USE_I18N = True
USE_L10N = True
USE_TZ = True


# ***************************************
#      Статични и медийни файлове
# ***************************************
# frontend/ = source (в git). static/ = изход на collectstatic (извън git).
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [BASE_DIR / 'frontend']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Максимален размер на тялото на заявката и качваните файлове (по подразбиране 100MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = env.int('DATA_UPLOAD_MAX_MEMORY_SIZE', default=104857600)  # 100 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = env.int('FILE_UPLOAD_MAX_MEMORY_SIZE', default=10485760)   # 10 MB
