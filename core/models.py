from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Абстрактный базовый класс, Требуется имя пользователя и пароль.
    Другие поля являются необязательными."""
    username = models.CharField(max_length=255, unique=True)
    pass