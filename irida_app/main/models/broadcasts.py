"""
Модели за броадкаст съобщения и системни известия.
"""

from django.contrib.auth.models import User
from django.db import models


class BroadcastMessage(models.Model):
    AUDIENCE_ALL = 0
    AUDIENCE_TEACHER = 4
    AUDIENCE_STUDENT = 5
    AUDIENCE_ADMIN = 1

    AUDIENCE_CHOICES = [
        (AUDIENCE_ALL, 'Всички потребители'),
        (AUDIENCE_TEACHER, 'Учители'),
        (AUDIENCE_STUDENT, 'Ученици'),
        (AUDIENCE_ADMIN, 'Администратори'),
    ]

    title = models.CharField('Заглавие', max_length=200)
    message = models.TextField('Текст на съобщението')
    target_role = models.PositiveSmallIntegerField(
        'Целева група',
        choices=AUDIENCE_CHOICES,
        default=AUDIENCE_ALL,
        help_text='Роля на потребителите, до които е адресирано съобщението'
    )
    is_active = models.BooleanField('Активно', default=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Създадено от',
        related_name='authored_broadcasts'
    )
    created_at = models.DateTimeField('Създадено на', auto_now_add=True)
    expires_at = models.DateTimeField('Валидно до', null=True, blank=True)

    class Meta:
        verbose_name = 'Броадкаст съобщение'
        verbose_name_plural = 'Броадкаст съобщения'
        ordering = ['-created_at', '-id']

    def __str__(self):
        return self.title


class BroadcastMessageRead(models.Model):
    message = models.ForeignKey(
        BroadcastMessage,
        on_delete=models.CASCADE,
        related_name='reads',
        verbose_name='Съобщение'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='read_broadcasts',
        verbose_name='Потребител'
    )
    read_at = models.DateTimeField('Прочетено на', auto_now_add=True)

    class Meta:
        verbose_name = 'Прочетено броадкаст съобщение'
        verbose_name_plural = 'Прочетени броадкаст съобщения'
        constraints = [
            models.UniqueConstraint(fields=['message', 'user'], name='unique_user_broadcast_read')
        ]

    def __str__(self):
        return f'{self.user.username} - {self.message.title}'
