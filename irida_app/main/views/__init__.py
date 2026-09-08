"""
View-та на приложение `main`, групирани по предназначение:

    auth.py            вход/изход
    pages.py           HTML страници (server-rendered)
    api_context.py     контекст на текущия потребител + избори по подразбиране
    api_schools.py     училища и специалности
    api_curriculum.py  предмети, цели, раздели, теми
    api_lessons.py     уроци, точки от плана, бележки, задачи
    api_uploads.py     качване на картинки от WYSIWYG редакторите
    api_users.py       управление на потребители

Реекспортът пази `from main.views import login_view`.
"""

from .api_context import (
    UserDataAPIView,
    UserDataExpandedAPIView,
    set_course,
    set_grade_section,
    set_session,
    set_speciality,
    set_subject,
)
from .api_curriculum import (
    GoalUpsertView,
    SpecialtySubjectsView,
    SubjectGoalsView,
    SubjectUnitsWithTopicsView,
    TopicUpsertView,
    UnitUpsertView,
    subject_detail,
)
from .api_lessons import (
    SessionListCreateView,
    SessionNotesForSessionView,
    SessionPointsForSessionView,
    SessionRetrieveUpdateDestroyView,
    SessionTasksForSessionView,
    SessionTopicListCreateView,
    SessionTopicRetrieveUpdateDestroyView,
    SessionTopicsForSessionView,
    SubjectSessionsWithTopicsView,
    session_note_delete,
    session_note_upsert,
    session_point_delete,
    session_point_upsert,
    session_task_delete,
    session_task_upsert,
)
from .api_schools import (
    SchoolDetailAPIView,
    SchoolSpecialtiesView,
    specialty_detail,
)
from .api_uploads import ckeditor_image_upload, tinymce_image_upload
from .api_users import (
    UserListCreateView,
    UserListView,
    UserRetrieveUpdateDestroyView,
)
from .auth import login_view, logout_view, sign_in
from .pages import (
    course_goals_view,
    course_lessons_view,
    course_units_view,
    lesson_view,
    make_user_context,
    schools_list_view,
    session_home_view,
    session_list_view,
    session_main_view,
    session_main_view_old,
    specialties_list_view,
    subjects_list_view,
    users_list_view,
    welcome_view,
)

__all__ = [
    # auth
    'login_view',
    'logout_view',
    'sign_in',
    # pages
    'make_user_context',
    'welcome_view',
    'subjects_list_view',
    'users_list_view',
    'specialties_list_view',
    'schools_list_view',
    'course_goals_view',
    'course_units_view',
    'course_lessons_view',
    'session_home_view',
    'session_list_view',
    'session_main_view',
    'session_main_view_old',
    'lesson_view',
    # api_context
    'UserDataAPIView',
    'UserDataExpandedAPIView',
    'set_speciality',
    'set_subject',
    'set_grade_section',
    'set_session',
    'set_course',
    # api_schools
    'SchoolDetailAPIView',
    'SchoolSpecialtiesView',
    'specialty_detail',
    # api_curriculum
    'SpecialtySubjectsView',
    'subject_detail',
    'SubjectGoalsView',
    'GoalUpsertView',
    'SubjectUnitsWithTopicsView',
    'UnitUpsertView',
    'TopicUpsertView',
    # api_lessons
    'SessionListCreateView',
    'SessionRetrieveUpdateDestroyView',
    'SubjectSessionsWithTopicsView',
    'SessionTopicListCreateView',
    'SessionTopicRetrieveUpdateDestroyView',
    'SessionTopicsForSessionView',
    'SessionPointsForSessionView',
    'session_point_upsert',
    'session_point_delete',
    'SessionNotesForSessionView',
    'session_note_upsert',
    'session_note_delete',
    'SessionTasksForSessionView',
    'session_task_upsert',
    'session_task_delete',
    # api_uploads
    'ckeditor_image_upload',
    'tinymce_image_upload',
    # api_users
    'UserListView',
    'UserListCreateView',
    'UserRetrieveUpdateDestroyView',
]
