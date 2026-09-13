"""
Училища/организации, специалности и прикачени документи.
"""

from django.db import models

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
    attachment = models.FileField('Файл', upload_to='docs/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документи'
