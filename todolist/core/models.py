from django.contrib.auth.models import AbstractUser
#from django.db import models


class User(AbstractUser):
    pass
    # list_display = ('last_name', 'first_name', 'username', 'email')
    # list_filter = ('last_name', 'first_name', 'username', 'email')
    #
    # class Meta:
    #     verbose_name = 'Пользователь'
    #     verbose_name_plural = 'Пользователи'