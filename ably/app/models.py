from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(default='', max_length=20)
    phone = models.CharField(default='', max_length=11)
