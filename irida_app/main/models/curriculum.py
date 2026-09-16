"""
Учебна програма: предмет -> раздели -> теми, плюс цели на обучението.
"""

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# ***************************************
#        Предмети
# ***************************************
class Subject(models.Model):
    name = models.CharField('Име', max_length=200)
    grade = models.SmallIntegerField('Клас', default=12, validators=[ MinValueValidator(8), MaxValueValidator(12) ])
    subject_type = models.CharField('Тип', max_length=10, choices=[('теория', 'теория'), ('практика', 'практика')], default='теория',)
    hpy = models.PositiveIntegerField('Брой часове годишно', default=54, validators=[MinValueValidator(18)])
    wpy = models.SmallIntegerField('Брой учебни седмици годишно', choices=[(11,11), (18,18), (27,27), (29,29), (36,36)], default=18)
    hpw1 = models.SmallIntegerField('Брой часове седмично (1-ви срок)', default=0)
    hpw2 = models.SmallIntegerField('Брой часове седмично (2-ри срок)', default=0)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='creator_subject')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Учебен предмет'
        verbose_name_plural = 'Учебни предмети'
        ordering = ['name', '-subject_type']


# раздели за определен предмет (УП)
class Unit(models.Model):
    num = models.SmallIntegerField('Раздел №', default=1, validators=[ MinValueValidator(1)])
    name = models.CharField('Име', max_length=200)
    hours = models.SmallIntegerField('Мин. брой часове', default=1, validators=[ MinValueValidator(1)])
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_unit')

    def __str__(self):
        return f'Раздел {self.num}: {self.name}'

    class Meta:
        verbose_name = 'Раздел от УП'
        verbose_name_plural = 'Раздели от УП'


# точки по раздел от УП
class Topic(models.Model):
    num = models.SmallIntegerField('Раздел №', default=1, validators=[ MinValueValidator(1)])
    name = models.CharField('Име', max_length=200)
    MoSCoW_cat = models.CharField('MoSCoW категория', default='', max_length=1, blank=True,
                                  choices=[('M', 'must'), ('S', 'should'), ('C', 'could'), ('W', 'won`t')],)
    MoSCoW_rem = models.TextField('MoSCoW обосновка', default='', blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='unit_topic')

    def __str__(self):
        return f'{self.num}. {self.name}'

    class Meta:
        verbose_name = 'Тема от раздел на УП'
        verbose_name_plural = 'Теми от раздел на УП'


# Цели на обучението по учебен предмет
class Goal(models.Model):
    num = models.SmallIntegerField('Раздел №', default=1, validators=[ MinValueValidator(1)])
    name = models.CharField('Име', max_length=200)
    course = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='course_goals')

    def __str__(self):
        return f'{self.num}. {self.name}'

    class Meta:
        verbose_name = 'Цел на обучението'
        verbose_name_plural = 'Цели на обучението'
