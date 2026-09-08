"""
Development настройки. Ползват се по подразбиране от manage.py.
"""

from .base import *  # noqa: F401,F403
from .base import env

DEBUG = True

# В dev приемаме заявки само отвътре. Ако тестваш от телефон в локалната
# мрежа, добави IP-то в DJANGO_ALLOWED_HOSTS в .env.
ALLOWED_HOSTS = env.list(
    'DJANGO_ALLOWED_HOSTS',
    default=['localhost', '127.0.0.1', '[::1]'],
)

# В dev ключът може да има default - в prod не може.
SECRET_KEY = env(
    'DJANGO_SECRET_KEY',
    default='django-insecure-dev-only-5tfv6p%g4n%cpa&r4jq=o%z8gulfg3k&@1en',
)

# Пощата отива в конзолата вместо в реален SMTP.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Пълни SQL/шаблонни грешки в конзолата.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {'format': '{levelname} {asctime} {name} {message}', 'style': '{'},
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'simple'},
    },
    'root': {'handlers': ['console'], 'level': 'INFO'},
    'loggers': {
        'django.db.backends': {
            # Смени на 'DEBUG', за да видиш всяка SQL заявка.
            'level': env('DJANGO_SQL_LOG_LEVEL', default='WARNING'),
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

# django-debug-toolbar е опционален - проектът тръгва и без него.
try:
    import debug_toolbar  # noqa: F401
except ImportError:
    pass
else:
    INSTALLED_APPS += ['debug_toolbar']  # noqa: F405
    # Toolbar-ът трябва да е възможно най-нагоре, но след SecurityMiddleware.
    MIDDLEWARE.insert(1, 'debug_toolbar.middleware.DebugToolbarMiddleware')  # noqa: F405
    INTERNAL_IPS = ['127.0.0.1', '::1']
