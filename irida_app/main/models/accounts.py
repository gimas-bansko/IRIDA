"""
Профил на потребител (разширява django.contrib.auth.User) и лог на действията.
"""

import logging

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from ..constants import DARK, STUDENT, THEME_TYPE, USER_LEVEL
from .curriculum import Subject
from .lessons import Session
from .schools import School, Specialty

logger = logging.getLogger(__name__)


# ***************************************
#             Потребители
# ***************************************
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.BooleanField('Пол', default=True, choices=[(True, 'мъж'), (False, 'жена'), ] )
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='user_school', verbose_name='училище',
                               null=True, blank=True)
    access_level = models.PositiveSmallIntegerField('Роля', choices=USER_LEVEL, default=STUDENT,
                                                    help_text='роля (ниво на достъп)')
    session_screen = models.PositiveSmallIntegerField('Интерфейс', choices=THEME_TYPE, default=DARK,
                                                      help_text='цветова схема на интерфейса')
    grade = models.PositiveSmallIntegerField('Клас', default=11,
                                             validators=[MinValueValidator(8), MaxValueValidator(12)])
    section = models.CharField('Паралелка', max_length=1, default='а',
                               validators=[MinValueValidator('а'), MaxValueValidator('я')])
    speciality = models.ForeignKey(Specialty, verbose_name='Специалност', on_delete=models.SET_NULL, related_name='user_speciality',
                                   help_text='специалност по подразбиране', null=True, blank=True)
    subject = models.ForeignKey(Subject, verbose_name='Предмет', on_delete=models.SET_NULL, related_name='user_subject',
                                   help_text='учебен предмет по подразбиране', null=True, blank=True)
    session = models.ForeignKey(Session, verbose_name='Занятие', on_delete=models.SET_NULL, related_name='user_session',
                                   help_text='занятие по подразбиране', null=True, blank=True)

    def __str__(self):
        return f'Потребител #{self.user.id}: {self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name = 'Пофил на потребител'
        verbose_name_plural = 'Пофили на потребител'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    logger.debug('post_save(User): create profile, created=%s', created)
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    logger.debug('post_save(User): save profile')
    instance.userprofile.save()


# ***************************************
#         Логове
# ***************************************
class Log(models.Model):
    user_id = models.IntegerField('id на потребител', default=0)
    user_name = models.CharField('Име на потребител', max_length=50, default='', null=True)
    action = models.CharField('Действие', max_length=200, default='')
    date = models.DateTimeField('Дата и час', default=timezone.now, null=True)

    def __str__(self):
        return '('+str(self.date)+') '+self.user_name+'/ '+self.action

    class Meta:
        verbose_name = 'Действие'
        verbose_name_plural = 'Действия'
