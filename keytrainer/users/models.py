from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    """User model."""
    email = models.EmailField(unique=True)
    # настройки
    random_words = models.BooleanField(default=True)
    words_count = models.PositiveIntegerField(default=5)
