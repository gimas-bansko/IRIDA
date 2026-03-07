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
    path('goals', course_goals_view, name='goals_list'),
    path('units', course_units_view, name='units_list'),
    path('lessons', course_lessons_view, name='lessons_list'),
    path('users', users_list_view, name='users_list'),
    path('lesson/<int:session_id>/', lesson_view, name='lesson_details'),
    path('session_home', session_home_view, name='session_menu'),
    path('session_list', session_list_view, name='session_list'),
    path('session_main', session_main_view, name='session_main'),
    path('session_main_old', session_main_view, name='session_main_old'),


    # API
    path('api/context/', UserDataAPIView.as_view()),
    path('api/context/expanded/', UserDataExpandedAPIView.as_view()),

    path('api/schools/<int:pk>/', SchoolDetailAPIView.as_view(), name='school-detail'),
    path('api/schools/<int:school_id>/specialties/', SchoolSpecialtiesView.as_view(), name='school-specialties'),
    path('api/schools/<int:school_id>/specialty/<int:specialty_id>/', specialty_detail, name='school-specialty-detail'),

    path('api/specialty/<int:specialty_id>/', specialty_detail, name='specialty_detail'),
    path('api/speciality_select/<int:sp>/', set_speciality, name='set_speciality'),

    path('api/subject_select/<int:sb>/', set_subject, name='set_subject'),
    path('api/grade_section_select/<int:gr>/<int:se>/', set_grade_section, name='set_grade_section'),
    path('api/grade_section_select/', set_grade_section),
    path('api/session_select/<int:se>/', set_session, name='set_session'),

    path('api/specialty/<int:sp_id>/subjects/', SpecialtySubjectsView.as_view(), name='specialty-subjects'),
    path('api/specialty/<int:sp_id>/subjects/<int:subject_id>/', subject_detail, name='specialty-subjects-detail'),

    path('api/course_set/<int:sb>/', set_course, name='set_course'),
    path('api/course/<int:sb_id>/goals/', SubjectGoalsView.as_view(), name='subject-goals'),
    path('api/goals/upsert/', GoalUpsertView.as_view(), name='goal-upsert'),
    path('api/subjects/<int:subject_id>/units-with-topics/', SubjectUnitsWithTopicsView.as_view(), name='subject-units-with-topics'),
    path('api/units/upsert/', UnitUpsertView.as_view(), name='unit-upsert'),
    path('api/topics/upsert/', TopicUpsertView.as_view(), name='topic-upsert'),

    # Sessions
    path('api/sessions/', SessionListCreateView.as_view(), name='session-list-create'),
    path('api/sessions/<int:pk>/', SessionRetrieveUpdateDestroyView.as_view(), name='session-detail'),

    # Sessions for Subject with topics expanded
    path('api/subjects/<int:subject_id>/sessions-with-topics/', SubjectSessionsWithTopicsView.as_view(),
         name='subject-sessions-with-topics'),

    # SessionTopics
    path('api/session-topics/', SessionTopicListCreateView.as_view(), name='session-topic-list-create'),
    path('api/session-topics/<int:pk>/', SessionTopicRetrieveUpdateDestroyView.as_view(), name='session-topic-detail'),
    path('api/sessions/<int:session_id>/topics/', SessionTopicsForSessionView.as_view(), name='session-topics-for-session'),
    path('api/sessions/<int:session_id>/points/', SessionPointsForSessionView.as_view(), name='session-points-for-session'),
    path('api/session-points/upsert/', session_point_upsert, name='session-point-upsert'),
    path('api/session-points/<int:pk>/', session_point_delete, name='session-point-delete'),

    # SessionNotes
    path('api/sessions/<int:session_id>/notes/', SessionNotesForSessionView.as_view(),
         name='session-notes-for-session'),
    path('api/session-notes/upsert/', session_note_upsert, name='session-note-upsert'),
    path('api/session-notes/<int:pk>/', session_note_delete, name='session-note-delete'),

    # SessionTasks
    path('api/sessions/<int:session_id>/tasks/', SessionTasksForSessionView.as_view(),
         name='session-tasks-for-session'),
    path('api/session-tasks/upsert/', session_task_upsert, name='session-task-upsert'),
    path('api/session-tasks/<int:pk>/', session_task_delete, name='session-task-delete'),

    path('api/uploads/ckeditor-image/', ckeditor_image_upload, name='ckeditor-image-upload'),
    path('api/uploads/tinymce-image/', tinymce_image_upload, name='tinymce-image-upload'),

    path('api/users-list/<int:sc>/<int:lvl>/', UserListView.as_view(), name='users-list'),
    path('api/users/', UserListCreateView.as_view(), name='users-list-create'),
    path('api/users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
]
