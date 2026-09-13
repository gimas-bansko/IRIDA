"""
HTML маршрути. API-то е изнесено в api_urls.py.

Имената на маршрутите (name=...) са същите като преди разделянето -
{% url %} в шаблоните и fetch() в frontend/irida/js не се променят.
"""

from django.urls import include, path

from .views import (
    course_goals_view,
    course_lessons_view,
    course_units_view,
    lesson_view,
    login_view,
    logout_view,
    school_day_view,
    schools_list_view,
    session_home_view,
    session_list_view,
    session_main_view,
    specialties_list_view,
    student_lessons_view,
    subjects_list_view,
    users_list_view,
    welcome_view,
)

urlpatterns = [
    path('', login_view, name='home_login'),
    path('home', welcome_view, name='home'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),

    path('student_lessons', student_lessons_view, name='student_lessons'),
    path('student', student_lessons_view, name='student'),
    path('specialties', specialties_list_view, name='specialty_list'),
    path('subjects', subjects_list_view, name='subjects_list'),
    path('schools', schools_list_view, name='schools_list'),
    path('school_day', school_day_view, name='school_day'),
    path('goals', course_goals_view, name='goals_list'),
    path('units', course_units_view, name='units_list'),
    path('lessons', course_lessons_view, name='lessons_list'),
    path('users', users_list_view, name='users_list'),
    path('lesson/<int:session_id>/', lesson_view, name='lesson_details'),
    path('session_home', session_home_view, name='session_menu'),
    path('session_list', session_list_view, name='session_list'),
    path('session_main', session_main_view, name='session_main'),
    # ВНИМАНИЕ: сочи към session_main_view, не към session_main_view_old -
    # така беше и преди разделянето, запазено е.
    path('session_main_old', session_main_view, name='session_main_old'),

    path('api/', include('main.api_urls')),
]
