from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager

class User(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name='이름')
    username =  models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)
    objects = UserManager()

    def get_username(self) -> str:
        return self.username