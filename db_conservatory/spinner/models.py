from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models


import requests

class Database(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    image = models.CharField(max_length=255)
    ports = models.CommaSeparatedIntegerField(max_length=50)

    def __unicode__(self):
        return self.name

    def create_container(self, session_key):
        r = requests.post('http://%s/containers' % settings.SPIN_DOCKER_HOST)
        container_info = r.json()['container']
        container = Container(container_id=container_info['id'],
            name=container_info['name'].replace('_', ' ')[1:],
            uri=container_info['uri'],
            database=self,
            session_key=session_key,
            )
        container.save()
        return container

    def get_create_url(self):
        return reverse('create', kwargs={'database': self.slug})

class Container(models.Model):
    container_id = models.CharField(primary_key=True, unique=True, max_length=100)
    name = models.CharField(max_length=50)
    uri = models.URLField(max_length=200)
    database = models.ForeignKey(Database)
    session_key = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s %s (%s)" % (self.name.capitalize(), self.container_id, self.database)

    def get_absolute_url(self):
        return reverse('container', kwargs={'container_id': self.container_id})

    def get_spin_docker_info(self):
        r = requests.get('http://%s%s' % (settings.SPIN_DOCKER_HOST, self.uri))
        spin_docker_info = r.json()
        return spin_docker_info

    def is_running(self):
        return self.get_spin_docker_info()['container']['status'] == 'running'
