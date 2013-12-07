from django.contrib.auth.models import User
from django.db import models

class DBCUser(models.Model):
    user = models.OneToOneField(User)