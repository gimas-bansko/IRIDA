from django.urls import path, include
from .views import *

urlpatterns = [
    path('', login_view, name='home_login'),
    path('home', welcome_view, name='home'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),

    path('specialties', specialties_list_view, name='specialty_list'),
    path('subjects', subjects_list_view, name='subjects_list'),
    path('schools', schools_list_view, name='schools_list'),

    # API
    path('api/context/', UserDataAPIView.as_view()),
    path('api/schools/<int:pk>/', SchoolDetailAPIView.as_view(), name='school-detail'),
    path('api/schools/<int:school_id>/specialties/', SchoolSpecialtiesView.as_view(), name='school-specialties'),
    path('api/specialty/<int:specialty_id>/', specialty_detail, name='specialty_detail'),
    path('api/schools/<int:school_id>/specialty/<int:specialty_id>/', specialty_detail, name='school-specialty-detail'),
    path('api/speciality_select/<int:sp>/', set_speciality, name='set_speciality'),
]
