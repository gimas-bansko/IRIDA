"""
Приложения / файлове за цялото приложение (глобални документи и материали).
"""

import os
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from ..utils import app_attachment_upload_path


class AppAttachment(models.Model):
    num = models.SmallIntegerField('№', default=1, validators=[MinValueValidator(1)])
    name = models.CharField('Име / Заглавие', max_length=200, blank=True, default='')
    file = models.FileField('Файл', upload_to=app_attachment_upload_path, blank=True, null=True)
    original_filename = models.CharField('Оригинално име на файла', max_length=255, blank=True, default='')
    description = models.TextField('Коментар / Описание', default='', blank=True, help_text='Коментар или описание на файла')
    is_system = models.BooleanField('Системен файл / приложение', default=False)
    created_by = models.ForeignKey(
        User,
        verbose_name='Създаден от',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='app_attachments'
    )
    created_at = models.DateTimeField('Създаден на', auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField('Обновен на', auto_now=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.file and not self.original_filename:
            self.original_filename = os.path.basename(self.file.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.id} {self.name or self.original_filename or (self.file.name if self.file else "")}'

    class Meta:
        verbose_name = 'Приложение / Файл'
        verbose_name_plural = 'Приложения / Файлове'
        ordering = ['num', 'id']
