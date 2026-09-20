"""
Училища/организации, специалности и прикачени документи.
"""

import re
from django.db import models

from ..utils import (
    document_upload_path,
    get_safe_ascii_extension,
    specialty_plan_upload_path,
)
from .curriculum import Subject


# ***************************************
#                Специалности
# ***************************************
class Specialty(models.Model):

    specialty_type = models.CharField('Тип', max_length=15,
                                      choices=[('професия', 'професия'), ('специалност', 'специалност')],
                                      default='специалност')
    specialty_num = models.CharField('Специалност - номер', max_length=8, default='', blank=True)
    specialty_name = models.CharField('Специалност - име', max_length=100, default='', blank=True)
    level = models.PositiveSmallIntegerField(choices=[(2, 'втора'), (3, 'трета')], default=3,
                                             help_text='Степен на професионална квалификация')
    subjects = models.ManyToManyField(Subject, verbose_name='Предмети', blank=True)

    def __str__(self):
        return f'{self.specialty_num}: {self.specialty_name}'

    class Meta:
        verbose_name = 'Специалност'
        verbose_name_plural = 'Специалности'


# ***************************************
#                Училища
# ***************************************
def school_pic_path(instance, filename):
    safe_ext = get_safe_ascii_extension(filename) or '.png'
    raw_ident = instance.id if instance.id is not None else (instance.short_name or 'logo')
    safe_ident = re.sub(r'[^a-zA-Z0-9_-]', '', str(raw_ident)) or 'logo'
    new_filename = f"school_logo_{safe_ident}{safe_ext}"
    return f"sys_pics/{new_filename}"


class School(models.Model):
    short_name = models.CharField('Абревиатура', max_length=20, default='', blank=True,
                                  help_text='Съкратено име на училището')
    full_name = models.TextField('Име', default='', blank=True, help_text='Пълно име на училището')
    city = models.CharField('Населено място', max_length=50, default='', blank=True,
                            help_text='Населено място, където се намира училището')
    logo = models.ImageField('Лого', upload_to=school_pic_path, blank=True)
    address = models.CharField('Адрес', max_length=50, default='', blank=True,
                            help_text='Адрес в населеното място (ул. ... №...)')
    phone_number = models.CharField('Телефон', max_length=15, default='', blank=True)
    email = models.CharField('e-mail', max_length=35, default='', blank=True)
    boss = models.CharField('Директор', max_length=50, default='', blank=True,
                            help_text='Име на директора на училището')
    specialities = models.ManyToManyField(Specialty, verbose_name='Специалности', blank=True)

    def __str__(self):
        return f'{self.short_name} {self.city}'

    class Meta:
        verbose_name = 'Училище/организация'
        verbose_name_plural = 'Училища/организации'


# ***************************************
#             Документи
# ***************************************
class Documents(models.Model):
    title = models.CharField('Име', max_length=200)
    attachment = models.FileField('Файл', upload_to=document_upload_path)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документи'


# ***************************************
#       Параметри на учебния ден
# ***************************************
class SchoolDayConfig(models.Model):
    school_day_start = models.CharField(
        'Начален час на първия учебен час',
        max_length=5,
        default='08:00',
        help_text='Начален час във формат HH:MM (напр. 08:00)',
    )
    school_lessons_count = models.PositiveSmallIntegerField(
        'Брой учебни часове дневно',
        default=7,
        help_text='Брой учебни часове в рамките на един учебен ден',
    )
    lesson_duration_minutes = models.PositiveSmallIntegerField(
        'Продължителност на учебния час (минути)',
        default=45,
        help_text='Продължителност на един учебен час в минути',
    )
    first_break_duration_minutes = models.PositiveSmallIntegerField(
        'Продължителност на първото междучасие (минути)',
        default=20,
        help_text='Продължителност на първото (голямо) междучасие в минути',
    )
    regular_break_duration_minutes = models.PositiveSmallIntegerField(
        'Продължителност на останалите междучасия (минути)',
        default=10,
        help_text='Продължителност на останалите (малки) междучасия в минути',
    )

    def __str__(self):
        return f'Параметри на учебния ден (начало: {self.school_day_start}, часове: {self.school_lessons_count})'

    class Meta:
        verbose_name = 'Параметри на учебния ден'
        verbose_name_plural = 'Параметри на учебния ден'

    @classmethod
    def get_config(cls):
        config = cls.objects.first()
        if not config:
            config = cls.objects.create(
                school_day_start='08:00',
                school_lessons_count=7,
                lesson_duration_minutes=45,
                first_break_duration_minutes=20,
                regular_break_duration_minutes=10,
            )
        return config
