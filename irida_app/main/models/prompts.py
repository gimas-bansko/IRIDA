"""
Модели за управление на AI промптове (шаблони за учители).
"""
from django.contrib.auth.models import User
from django.db import models


class AIPrompt(models.Model):
    PAGE_CHOICES = [
        ('general', 'Общи промптове'),
        ('course_goals', 'Цели на курс/предмет'),
        ('course_units', 'Учебни раздели/модули'),
        ('course_lessons', 'Теми за уроци'),
        ('session_list', 'Списък с уроци'),
        ('lesson_main', 'Подготовка на урок / занятие'),
        ('school_day', 'Учебен ден и програма'),
    ]

    title = models.CharField('Заглавие / Име', max_length=200)
    page_key = models.CharField(
        'Страница / Контекст',
        max_length=50,
        choices=PAGE_CHOICES,
        default='general',
        db_index=True
    )
    prompt_text = models.TextField(
        'Текст на промпта',
        help_text='Поддържа плейсхолдъри: {предмет}, {тема}, {цели}, {фокус}, {точки}, {клас}, {специалност}'
    )
    instructions = models.TextField(
        'Указания за ползване',
        blank=True,
        default='',
        help_text='Препоръки за очакван резултат и настройки на AI модела'
    )
    is_system = models.BooleanField('Системен шаблон', default=False)
    order = models.SmallIntegerField('Подредба', default=1)
    created_by = models.ForeignKey(
        User,
        verbose_name='Създаден от',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ai_prompts'
    )
    created_at = models.DateTimeField('Създаден на', auto_now_add=True)
    updated_at = models.DateTimeField('Обновен на', auto_now=True)

    class Meta:
        app_label = 'main'
        verbose_name = 'AI Промпт'
        verbose_name_plural = 'AI Промптове'
        ordering = ['page_key', 'order', 'title']

    def __str__(self):
        return f"{self.title} ({self.get_page_key_display()})"
