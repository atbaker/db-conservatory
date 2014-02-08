from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

import spindocker

DATABASE_CATEGORY_CHOICES = (
    ('BS', 'Base'),
    ('CM', 'Custom'),
    ('DS', 'Dataset'),
)

class Database(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=2, choices=DATABASE_CATEGORY_CHOICES, default='BS')
    short_description = models.TextField(blank=True)
    long_description = models.TextField(blank=True)
    image = models.CharField(max_length=255)
    order = models.IntegerField(null=True, blank=True)
    ports = models.CommaSeparatedIntegerField(max_length=50)
    active = models.BooleanField(default=True)
    login_prompt = models.TextField(blank=True)
    db_command = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.name

    def create_container(self, session_key=None, user=None):
        data = {'image': self.image, 'port': eval(self.ports)}
        container_info = spindocker.post('containers', data)
        container = Container(container_id=container_info['id'],
            name=container_info['name'].replace('_', ' ')[1:].capitalize(),
            uri=container_info['uri'],
            database=self,
            session_key=session_key,
            user=user,
            )
        container.save()
        return container

    def get_create_url(self):
        return reverse('create', kwargs={'database': self.image})

class Container(models.Model):
    container_id = models.CharField(primary_key=True, unique=True, max_length=100)
    name = models.CharField(max_length=50)
    uri = models.URLField(max_length=200)
    database = models.ForeignKey(Database)
    session_key = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, null=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s %s (%s)" % (self.name.capitalize(), self.container_id, self.database)

    def get_absolute_url(self):
        return reverse('container', kwargs={'container_id': self.container_id})

    def get_spin_docker_info(self):
        return spindocker.get(self.uri)

    def is_running(self):
        return self.get_spin_docker_info()['status'] == 'running'

    def start(self):
        data = {'status': 'running'}
        container_info = spindocker.patch(self.uri, data)
        return container_info

    def stop(self):
        data = {'status': 'stopped'}
        container_info = spindocker.patch(self.uri, data)
        return container_info

    def delete(self):
        spindocker.delete(self.uri)
        return super(Container, self).delete()
