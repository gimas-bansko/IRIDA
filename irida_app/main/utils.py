"""
Помощни функции.

Номенклатурите (USER_LEVEL, THEME_TYPE и т.н.) се преместиха в constants.py.
"""

import os

from django.utils import timezone


def session_image_upload_path(filename: str) -> str:
    """Път за качена картинка към точка от урок.

    ЗАСЕГА НЕ СЕ ПОЛЗВА - качването минава през ckeditor_image_upload() /
    tinymce_image_upload() във views/api_uploads.py, които записват директно
    в 'session_pics/<оригинално име>'. Тази функция дава уникално име по
    timestamp и би решила проблема с презаписване на файлове с еднакви имена.
    """
    _name, ext = os.path.splitext(filename)
    ts = timezone.now().strftime('%Y%m%d_%H%M%S_%f')
    safe_ext = (ext or '').lower()
    return f"session_pics/{ts}{safe_ext}"


def update_test_statistics(test_result, answers):
    """Актуализира статистиките за теста и въпросите.

    ВНИМАНИЕ: мъртъв код. Разчита на модел с полета .task.level,
    .task.update_statistics() и .average_difficulty, каквито в момента
    няма в models/. Оставено като скеле за планирания модул за тестове
    (виж TASK_TYPE / LEVEL_TYPE в constants.py).
    """
    total_difficulty = 0
    for answer in answers:
        # Актуализиране на статистиките за въпроса
        answer.task.update_statistics(answer.is_correct, answer.points)
        total_difficulty += answer.task.level

    # Актуализиране на средната трудност на теста
    test_result.average_difficulty = total_difficulty / len(answers)
    test_result.save()
