"""
Модели на приложение `main`, групирани по домейн.

Всички модели остават в един Django app (app_label='main'), затова
разбиването на модули НЕ променя имената на таблиците и НЕ изисква
нови миграции.

Реекспортът тук пази обратната съвместимост: `from main.models import Subject`
работи както преди.

Ред на импортите = ред на зависимостите:
    curriculum -> schools -> lessons -> accounts
"""

from .accounts import (
    Log,
    UserProfile,
    create_user_profile,
    save_user_profile,
)
from .curriculum import Goal, Subject, Topic, Unit
from .lessons import (
    Session,
    SessionAttachment,
    SessionNote,
    SessionPoint,
    SessionTask,
    SessionTopic,
)
from .schools import Documents, School, SchoolDayConfig, Specialty, school_pic_path

__all__ = [
    # curriculum
    'Subject',
    'Unit',
    'Topic',
    'Goal',
    # lessons
    'Session',
    'SessionTopic',
    'SessionPoint',
    'SessionNote',
    'SessionTask',
    'SessionAttachment',
    # schools
    'Specialty',
    'School',
    'SchoolDayConfig',
    'Documents',
    'school_pic_path',
    # accounts
    'UserProfile',
    'Log',
    'create_user_profile',
    'save_user_profile',
]
