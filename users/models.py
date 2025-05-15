from django.contrib.auth.models import AbstractUser
from django.db import models
from novels.models import Novel

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)
    is_author = models.BooleanField(default=False)

    def __str__(self):
        return self.username