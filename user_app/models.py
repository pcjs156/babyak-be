from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager

class User(AbstractUser):
    name = models.CharField(max_length=100)
    username =  models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)
    objects = UserManager()

    def get_username(self) -> str:
        return self.username