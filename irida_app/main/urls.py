from django.urls import path, include
from .views import *

urlpatterns = [
    path('', login_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('subjects', subjects_list_view, name='subject_list'),
    path('schools', schools_list_view, name='schools_list'),

    # API
    path('api/context/', UserDataAPIView.as_view()),
]
