"""
API маршрути. Включват се от urls.py под префикс 'api/'.
"""

from django.urls import path

from .views import (
    AIPromptListView,
    AIPromptUpsertView,
    AppAttachmentListView,
    CurriculumImportView,
    GoalImportView,
    GoalRetrieveUpdateDestroyView,
    GoalUpsertView,
    SchoolDayConfigAPIView,
    SchoolDetailAPIView,
    SchoolSpecialtiesView,
    SessionAttachmentsForSessionView,
    SessionImportView,
    SessionListCreateView,
    SessionNotesForSessionView,
    SessionPlanImportView,
    SessionPointsForSessionView,
    SessionRetrieveUpdateDestroyView,
    SessionTasksForSessionView,
    SessionAttachmentsForSessionView,
    SessionTopicListCreateView,
    SessionTopicRetrieveUpdateDestroyView,
    SessionTopicsForSessionView,
    SpecialtySubjectsView,
    SubjectGoalsView,
    SubjectSessionsWithTopicsView,
    SubjectUnitsWithTopicsView,
    TopicRetrieveUpdateDestroyView,
    TopicUpsertView,
    UnitRetrieveUpdateDestroyView,
    UnitUpsertView,
    UserDataAPIView,
    UserDataExpandedAPIView,
    UserListCreateView,
    UserListView,
    UserRetrieveUpdateDestroyView,
    ai_prompt_delete,
    app_attachment_delete,
    app_attachment_upsert,
    ckeditor_image_upload,
    session_attachment_delete,
    session_attachment_upsert,
    session_note_delete,
    session_note_upsert,
    session_point_delete,
    session_point_upsert,
    session_task_delete,
    session_task_upsert,
    set_course,
    set_grade_section,
    set_session,
    set_speciality,
    set_subject,
    specialty_detail,
    subject_detail,
    tinymce_image_upload,
)

urlpatterns = [
    # Контекст на текущия потребител
    path('context/', UserDataAPIView.as_view()),
    path('context/expanded/', UserDataExpandedAPIView.as_view()),

    # Училища
    path('schools/<int:pk>/', SchoolDetailAPIView.as_view(), name='school-detail'),
    path('schools/<int:school_id>/specialties/', SchoolSpecialtiesView.as_view(), name='school-specialties'),
    path('schools/<int:school_id>/specialty/<int:specialty_id>/', specialty_detail, name='school-specialty-detail'),
    path('school-day-config/', SchoolDayConfigAPIView.as_view(), name='school-day-config'),

    # Специалности
    path('specialty/<int:specialty_id>/', specialty_detail, name='specialty_detail'),
    path('speciality_select/<int:sp>/', set_speciality, name='set_speciality'),
    path('specialty/<int:sp_id>/subjects/', SpecialtySubjectsView.as_view(), name='specialty-subjects'),
    path('specialty/<int:sp_id>/subjects/<int:subject_id>/', subject_detail, name='specialty-subjects-detail'),

    # Избори по подразбиране за потребителя
    path('subject_select/<int:sb>/', set_subject, name='set_subject'),
    path('grade_section_select/<int:gr>/<int:se>/', set_grade_section, name='set_grade_section'),
    path('grade_section_select/', set_grade_section),
    path('session_select/<int:se>/', set_session, name='set_session'),

    # Предмети, цели, раздели, теми
    path('course_set/<int:sb>/', set_course, name='set_course'),
    path('course/<int:sb_id>/goals/', SubjectGoalsView.as_view(), name='subject-goals'),
    path('goals/upsert/', GoalUpsertView.as_view(), name='goal-upsert'),
    path('goals/<int:pk>/', GoalRetrieveUpdateDestroyView.as_view(), name='goal-detail'),
    path('subjects/<int:subject_id>/import-goals/', GoalImportView.as_view(), name='goal-import'),
    path('subjects/<int:subject_id>/units-with-topics/', SubjectUnitsWithTopicsView.as_view(), name='subject-units-with-topics'),
    path('subjects/<int:subject_id>/import-curriculum/', CurriculumImportView.as_view(), name='curriculum-import'),
    path('units/upsert/', UnitUpsertView.as_view(), name='unit-upsert'),
    path('units/<int:pk>/', UnitRetrieveUpdateDestroyView.as_view(), name='unit-detail'),
    path('topics/upsert/', TopicUpsertView.as_view(), name='topic-upsert'),
    path('topics/<int:pk>/', TopicRetrieveUpdateDestroyView.as_view(), name='topic-detail'),

    # Уроци
    path('subjects/<int:subject_id>/import-sessions/', SessionImportView.as_view(), name='session-import'),
    path('sessions/', SessionListCreateView.as_view(), name='session-list-create'),
    path('sessions/<int:pk>/', SessionRetrieveUpdateDestroyView.as_view(), name='session-detail'),

    # Уроци за предмет, с разгънати теми
    path('subjects/<int:subject_id>/sessions-with-topics/', SubjectSessionsWithTopicsView.as_view(),
         name='subject-sessions-with-topics'),

    # Теми към урок
    path('session-topics/', SessionTopicListCreateView.as_view(), name='session-topic-list-create'),
    path('session-topics/<int:pk>/', SessionTopicRetrieveUpdateDestroyView.as_view(), name='session-topic-detail'),
    path('sessions/<int:session_id>/topics/', SessionTopicsForSessionView.as_view(), name='session-topics-for-session'),

    # Точки от плана
    path('sessions/<int:session_id>/points/', SessionPointsForSessionView.as_view(), name='session-points-for-session'),
    path('sessions/<int:session_id>/import-plan/', SessionPlanImportView.as_view(), name='session-plan-import'),
    path('session-points/upsert/', session_point_upsert, name='session-point-upsert'),
    path('session-points/<int:pk>/', session_point_delete, name='session-point-delete'),

    # Бележки
    path('sessions/<int:session_id>/notes/', SessionNotesForSessionView.as_view(),
         name='session-notes-for-session'),
    path('session-notes/upsert/', session_note_upsert, name='session-note-upsert'),
    path('session-notes/<int:pk>/', session_note_delete, name='session-note-delete'),

    # Задачи
    path('sessions/<int:session_id>/tasks/', SessionTasksForSessionView.as_view(),
         name='session-tasks-for-session'),
    path('session-tasks/upsert/', session_task_upsert, name='session-task-upsert'),
    path('session-tasks/<int:pk>/', session_task_delete, name='session-task-delete'),

    # Приложения
    path('sessions/<int:session_id>/attachments/', SessionAttachmentsForSessionView.as_view(),
         name='session-attachments-for-session'),
    path('session-attachments/upsert/', session_attachment_upsert, name='session-attachment-upsert'),
    path('session-attachments/<int:pk>/', session_attachment_delete, name='session-attachment-delete'),
    path('app-attachments/', AppAttachmentListView.as_view(), name='app-attachment-list'),
    path('app-attachments/upsert/', app_attachment_upsert, name='app-attachment-upsert'),
    path('app-attachments/<int:pk>/', app_attachment_delete, name='app-attachment-delete'),

    # Качване на картинки
    path('uploads/ckeditor-image/', ckeditor_image_upload, name='ckeditor-image-upload'),
    path('uploads/tinymce-image/', tinymce_image_upload, name='tinymce-image-upload'),

    # Потребители
    path('users-list/<int:sc>/<int:lvl>/', UserListView.as_view(), name='users-list'),
    path('users/', UserListCreateView.as_view(), name='users-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),

    # AI Промптове
    path('prompts/', AIPromptListView.as_view(), name='prompt-list'),
    path('prompts/upsert/', AIPromptUpsertView.as_view(), name='prompt-upsert'),
    path('prompts/<int:pk>/', ai_prompt_delete, name='prompt-delete'),
]
