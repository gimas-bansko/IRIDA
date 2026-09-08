"""
WSGI config for the IRIDA project.

It exposes the WSGI callable as a module-level variable named ``application``.

За production сървърът трябва да подаде DJANGO_SETTINGS_MODULE=config.settings.prod
в обкръжението. Default-ът тук е dev, за да не тръгне prod случайно с dev настройки.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

application = get_wsgi_application()
