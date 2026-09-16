"""
Production настройки.

Стартиране:
    DJANGO_SETTINGS_MODULE=config.settings.prod

Задължителни променливи в обкръжението (няма default - ако липсват,
приложението отказва да стартира, вместо да тръгне несигурно):
    DJANGO_SECRET_KEY
    DJANGO_ALLOWED_HOSTS
    DB_PASSWORD
"""

from .base import *  # noqa: F401,F403
from .base import env

DEBUG = env.bool('DJANGO_DEBUG', default=False)

# Нарочно без default - празен ALLOWED_HOSTS при DEBUG=False е тиха повреда.
SECRET_KEY = env('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')

CSRF_TRUSTED_ORIGINS = env.list('DJANGO_CSRF_TRUSTED_ORIGINS', default=[])


# ***************************************
#             Сигурност
# ***************************************
# Приема се, че приложението стои зад HTTPS reverse proxy.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS. Започни с малка стойност (напр. 3600) и я вдигни, след като си
# сигурен, че HTTPS работи навсякъде - иначе рискуваш да си заключиш домейна.
SECURE_HSTS_SECONDS = env.int('DJANGO_SECURE_HSTS_SECONDS', default=3600)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = False


# ***************************************
#          Статични файлове
# ***************************************
# whitenoise раздава collectstatic изхода директно от Django.
# Ако статиката се раздава от nginx, махни middleware-а и STORAGES блока.
try:
    import whitenoise  # noqa: F401
except ImportError:
    pass
else:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')  # noqa: F405
    STORAGES = {
        'default': {
            'BACKEND': 'django.core.files.storage.FileSystemStorage',
        },
        'staticfiles': {
            'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
        },
    }


# ***************************************
#              Логове
# ***************************************
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {name} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'verbose'},
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'django_error.log',
            'formatter': 'verbose',
            'level': 'ERROR',
        },
    },
    'root': {'handlers': ['console'], 'level': 'INFO'},
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
