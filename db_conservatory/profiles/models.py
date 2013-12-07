from django.contrib.auth.models import AbstractUser
from django.db import models

class DBCUser(AbstractUser):
    max_containers = models.IntegerField(default=5)
