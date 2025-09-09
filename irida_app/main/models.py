from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from django.utils import timezone
from .utils import *
""" 
***************************************
        Предмети 
***************************************
"""
class Subject(models.Model):
    name = models.CharField('Име', max_length=200)
    grade = models.SmallIntegerField('Клас', default=12, validators=[ MinValueValidator(8), MaxValueValidator(12) ])
    subject_type = models.BooleanField('Тип', choices=[(True, 'теория'), (False, 'практика')], default=True,)
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
    MoSCoW_rem = models.CharField('MoSCoW обосновка', max_length=200, default='', blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='unit_topic')

    def __str__(self):
        return f'{self.num}. {self.name}'

    class Meta:
        verbose_name = 'Тема от раздел на УП'
        verbose_name_plural = 'Теми от раздел на УП'

# Цели на обучението по учебен предмет
class Goals(models.Model):
    num = models.SmallIntegerField('Раздел №', default=1, validators=[ MinValueValidator(1)])
    name = models.CharField('Име', max_length=200)
    course = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='course_goals')

    def __str__(self):
        return f'{self.num}. {self.name}'

    class Meta:
        verbose_name = 'Цел на обучението'
        verbose_name_plural = 'Цели на обучението'

# Задачи на обучението по предмет
class Objectives(models.Model):
    num = models.SmallIntegerField('Раздел №', default=1, validators=[ MinValueValidator(1)])
    name = models.CharField('Име', max_length=200)
    course = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='course_objectives')

    def __str__(self):
        return f'{self.num}. {self.name}'

    class Meta:
        verbose_name = 'Задачa на обучението'
        verbose_name_plural = 'Задачи на обучението'

"""
***************************************
            Клас
***************************************
"""
class Klass(models.Model):
    grade = models.PositiveSmallIntegerField('Клас', null=True, blank=True, default=11,
                                                     validators=[ MinValueValidator(8), MaxValueValidator(12) ] )
    section = models.CharField('Паралелка', null=True, blank=True, default='а', max_length=1)

    def __str__(self):
        return f'{self.grade} {self.section}'

    class Meta:
        verbose_name = 'Клас'
        verbose_name_plural = 'Класове'

""" 
***************************************
               Специалности
***************************************
"""
class Specialty(models.Model):

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

""" 
***************************************
               Училища
***************************************
"""
def school_pic_path(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"school_logo_{instance.id}.{ext}"
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
    classes = models.ManyToManyField(Klass, verbose_name='Класове', blank=True)

    def __str__(self):
        return f'{self.short_name} {self.city}'

    class Meta:
        verbose_name = 'Училище/организация'
        verbose_name_plural = 'Училища/организации'

""" 
***************************************
            Документи
***************************************
"""
class Documents(models.Model):
    title = models.CharField('Име', max_length=200)
    attachment = models.FileField('Файл', upload_to='docs/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документи'

"""
***************************************
            Потребители
***************************************
"""
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.BooleanField('Пол', default=True, choices=[(True, 'мъж'), (False, 'жена'), ] )
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='user_school', verbose_name='училище',
                               null=True, blank=True)
    access_level = models.PositiveSmallIntegerField('Роля', choices=USER_LEVEL, default=STUDENT,
                                                    help_text='роля (ниво на достъп)')
    session_screen = models.PositiveSmallIntegerField('Интерфейс', choices=THEME_TYPE, default=DARK,
                                                      help_text='цветова схема на интерфейса')
    grade_section = models.ForeignKey(Klass, verbose_name='Клас', on_delete=models.CASCADE, related_name='user_grade',
                                   help_text='клас по подразбиране', null=True, blank=True)
    speciality = models.ForeignKey(Specialty, verbose_name='Специалност', on_delete=models.CASCADE, related_name='user_speciality',
                                   help_text='специалност по подразбиране', null=True, blank=True)
    subject = models.ForeignKey(Subject, verbose_name='Предмет', on_delete=models.CASCADE, related_name='user_subject',
                                   help_text='учебен предмет по подразбиране', null=True, blank=True)

    def __str__(self):
        return f'Потребител #{self.user.id}: {self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name = 'Пофил на потребител'
        verbose_name_plural = 'Пофили на потребител'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    print('===>>> create user')
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    print('===>>> save user')
    instance.userprofile.save()


""" 
***************************************
        Логове 
***************************************
"""
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

