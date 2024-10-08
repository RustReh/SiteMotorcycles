from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    photo = models.ImageField(
        upload_to='users/%Y/',
        blank=True, null=True,
        verbose_name='Фотография профиля',
    )
