from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(null=True, blank=True)

    name = models.CharField(max_length=100, verbose_name='이름')
