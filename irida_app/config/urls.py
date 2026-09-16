from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^media_files/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# django-debug-toolbar се включва само в dev и само ако е инсталиран
# (dev.py го добавя в INSTALLED_APPS при същото условие).
if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
