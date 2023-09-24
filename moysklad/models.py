from django.db import models
from django.utils import timezone

class Auth(models.Model):
    email = models.CharField('Email', null=True, blank=True, max_length=100)
    password = models.CharField('Пароль', null=True, blank=True, max_length=250)
    is_active = models.BooleanField('Подключено',null=True, blank=True, default=False)
    pub_date = models.DateTimeField('Последнее обновления', null=True, blank=True)
    error = models.TextField('Лог', null=True, blank=True)
    class Meta:
        verbose_name = 'Аутентификация в Мой Склад'
        verbose_name_plural = 'Аутентификация в Мой Склад'

    def __str__(self):
        return str(self.email)

