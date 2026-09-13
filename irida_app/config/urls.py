from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
]

# Раздаване на качените файлове от Django. При DEBUG=False static()
# връща празен списък - в production media се раздава от nginx/whitenoise.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static('/media_files/', document_root=settings.MEDIA_ROOT)

# django-debug-toolbar се включва само в dev и само ако е инсталиран
# (dev.py го добавя в INSTALLED_APPS при същото условие).
if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
