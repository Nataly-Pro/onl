from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='почта', unique=True)
    first_name = models.CharField(max_length=280, verbose_name='имя')
    last_name = models.CharField(max_length=280, verbose_name='фамилия')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
