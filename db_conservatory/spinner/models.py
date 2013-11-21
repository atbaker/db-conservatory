from django.conf import settings
from django.db import models

import requests

class Database(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    image = models.CharField(max_length=255)
    ports = models.CommaSeparatedIntegerField(max_length=50)

    def create_container(self):
        r = requests.post('http://%s/containers' % settings.SPIN_DOCKER_HOST)
        return r.json()['container']
