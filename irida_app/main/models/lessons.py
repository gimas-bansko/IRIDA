"""
Урок/занятие: основна единица, темите към нея и точките от плана
с бележките и задачите им.
"""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .curriculum import Subject, Topic


# Урок - основен
class Session(models.Model):
    course = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='course_session')
    num = models.SmallIntegerField('Урок №', default=1, validators=[ MinValueValidator(1)])
    name = models.CharField('Име', max_length=200, help_text='Общо име на урока')
    focus = models.TextField('Фокус', default='', blank=True, help_text='Фокус(основни акценти на урока)')
    goals = models.TextField('Цели', default='', blank=True, help_text='Оосновни цели на урока')
    duration = models.SmallIntegerField('Продължителност', default=1, validators=[ MinValueValidator(1), MaxValueValidator(7)])
    session_type = models.CharField('Вид на урочната единица', default='', max_length=3, blank=True,
                                  choices=[('НЗ', 'Нови знания'), ('УПР', 'Упражнение'), ('ПК', 'Проверка и контрол'),
                                           ('ОС', 'Обобщаване и систематизиране'), ('K', 'Комбиниран урок')])
    basic_level = models.BooleanField('Тип на урока', default=True,
                                  choices=[(True, 'Основен(задължителен) урок'), (False, 'Резервен(при необходимост) урок')])
    collapsed = models.BooleanField('Показва се "свито"', default=True,
                                  choices=[(True, 'Да'), (False, 'Не')])

    def __str__(self):
        return f'{self.num}. {self.name}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроци'
        ordering = ['num', 'id']


# Урок - теми
class SessionTopic(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='session_topics', verbose_name='Занятие')
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name='topic_sessions', verbose_name='Тема')
    description = models.CharField('Описание', max_length=200, blank=True, default='')

    def __str__(self):
        return self.topic.name if self.topic_id else self.description

    class Meta:
        verbose_name = 'Урок (тема)'
        verbose_name_plural = 'Урок (теми)'
        constraints = [
            models.UniqueConstraint(fields=['session', 'topic'], name='unique_session_topic')
        ]


# Занятие - точки от плана
class SessionPoint(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='session_points', verbose_name='Занятие')
    num = models.SmallIntegerField('Занятие №', default=1, validators=[ MinValueValidator(1)])
    name = models.CharField('Текст(име)', max_length=200, blank=True, default='')
    description = models.CharField('Описание', max_length=200, blank=True, default='')
    duration = models.SmallIntegerField('Продължителност (мин.)', default=1,
                                        validators=[MinValueValidator(1), MaxValueValidator(270)])
    content = models.TextField('Съдържание', default='', blank=True, help_text='Съдържание на точката (html)')

    def __str__(self):
        return f'{self.id} {self.name}'

    class Meta:
        verbose_name = 'Точка от плана'
        verbose_name_plural = 'Точки от плана'


# Занятие - бележки към точка от план
class SessionNote(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='session_notes', verbose_name='Занятие')
    point = models.ForeignKey(SessionPoint, verbose_name='Точка от плана на урока', on_delete=models.SET_NULL,
                              null=True, blank=True,related_name='point_notes')
    num = models.SmallIntegerField('Бележка №', default=1, validators=[MinValueValidator(1)])
    name = models.CharField('Текст(име)', max_length=200, blank=True, default='')
    content = models.TextField('Съдържание', default='', blank=True, help_text='Съдържание на точката (html)')

    def __str__(self):
        return f'{self.id} {self.name}'

    class Meta:
        verbose_name = 'Бележка към точка от план'
        verbose_name_plural = 'Бележки към точка от план'


# Занятие - Задачи към точка от план
class SessionTask(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='session_tasks', verbose_name='Занятие')
    point = models.ForeignKey(SessionPoint, verbose_name='Задача към точка от план', on_delete=models.SET_NULL,
                              null=True, blank=True,related_name='point_tasks')
    num = models.SmallIntegerField('Бележка №', default=1, validators=[MinValueValidator(1)])
    name = models.CharField('Текст(име)', max_length=200, blank=True, default='')
    condition = models.TextField('Условие', default='', blank=True, help_text='Условие на задачата (html)')
    answer = models.TextField('Орговор', default='', blank=True, help_text='Отговор на задачата (html)')

    def __str__(self):
        return f'{self.id} {self.name}'

    class Meta:
        verbose_name = 'Задача към точка от план'
        verbose_name_plural = 'Задачи към точка от план'


# Занятие - Приложения (прикачени файлове - теория и други)
class SessionAttachment(models.Model):
    THEORY = 'theory'
    OTHER = 'other'
    ATTACHMENT_TYPE_CHOICES = [
        (THEORY, 'Теория'),
        (OTHER, 'Други'),
    ]

    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='session_attachments', verbose_name='Занятие')
    point = models.ForeignKey(SessionPoint, verbose_name='Точка от плана на урока', on_delete=models.SET_NULL,
                              null=True, blank=True, related_name='point_attachments')
    num = models.SmallIntegerField('№', default=1, validators=[MinValueValidator(1)])
    name = models.CharField('Име / Заглавие', max_length=200, blank=True, default='')
    attachment_type = models.CharField('Тип', max_length=20, choices=ATTACHMENT_TYPE_CHOICES, default=OTHER)
    file = models.FileField('Файл', upload_to='session_attachments/', blank=True, null=True)
    description = models.TextField('Коментар / Описание', default='', blank=True, help_text='Коментар или описание на файла')

    def __str__(self):
        return f'{self.id} {self.name or (self.file.name if self.file else "")}'

    class Meta:
        verbose_name = 'Приложение / Файл към занятие'
        verbose_name_plural = 'Приложения / Файлове към занятие'
        ordering = ['num', 'id']
