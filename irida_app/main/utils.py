"""
Помощни функции.

Номенклатурите (USER_LEVEL, THEME_TYPE и т.н.) се преместиха в constants.py.
"""

import os
import re
import uuid

from django.utils import timezone


def get_safe_ascii_extension(filename: str) -> str:
    """Извлича безопасно ASCII разширение на файл (напр. '.docx', '.pdf', '.png')."""
    if not filename:
        return ''
    _, ext = os.path.splitext(filename)
    if not ext:
        return ''
    safe_ext = re.sub(r'[^a-zA-Z0-9._-]', '', ext).lower()
    return safe_ext


def generate_unique_ascii_filename(filename: str, prefix: str = '') -> str:
    """
    Генерира случайно уникално име на файл само с ASCII символи (uuid4),
    запазвайки безопасното разширение на оригиналния файл.
    """
    ext = get_safe_ascii_extension(filename)
    unique_id = uuid.uuid4().hex
    if prefix:
        return f"{prefix}_{unique_id}{ext}"
    return f"{unique_id}{ext}"


def session_attachment_upload_path(instance, filename: str) -> str:
    """Път за качен файл към приложение на урок (без кирилица, с уникално име)."""
    unique_name = generate_unique_ascii_filename(filename)
    return f"session_attachments/{unique_name}"


def app_attachment_upload_path(instance, filename: str) -> str:
    """Път за качен файл към общо системно приложение (без кирилица, с уникално име)."""
    unique_name = generate_unique_ascii_filename(filename)
    return f"app_attachments/{unique_name}"


def session_image_upload_path(filename: str) -> str:
    """Път за качена картинка към точка от урок (без кирилица, с уникално име)."""
    unique_name = generate_unique_ascii_filename(filename, prefix='img')
    return f"session_pics/{unique_name}"


def document_upload_path(instance, filename: str) -> str:
    """Път за качен документ към училище/организация."""
    unique_name = generate_unique_ascii_filename(filename, prefix='doc')
    return f"docs/{unique_name}"


def specialty_plan_upload_path(instance, filename: str) -> str:
    """Път за качен учебен план към специалност."""
    unique_name = generate_unique_ascii_filename(filename, prefix='plan')
    return f"docs/{unique_name}"


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
