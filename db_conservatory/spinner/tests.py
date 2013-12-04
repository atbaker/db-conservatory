from django.test import TestCase
from django.test.client import Client
from .models import Database, Container
from .utils import get, post
from django.core.management import call_command

import responses

import pdb

class DatabaseTestCase(TestCase):
    def setUp(self):
        self.c = Client()

    def _create_database(self):
        db = Database.objects.create(name='MySQL',
            slug='mysql',
            image='mysqltoday',
            ports='3306,22')
        return db

    def _create_database_and_container(self, session_key='test'):
        responses.add(responses.POST, 'http://localhost:5000/v1/containers',
            body=u'{"db_port": "49154", "id": "ef458b3613b3", \
                "name": "/teal_lizard", "ssh_port": "49153", \
                "status": "running", "uri": "/v1/containers/ef458b3613b3", \
                "username": ""}',
            status=201)

        db = self._create_database()
        container = db.create_container(session_key)
        return container

    def test_database_attributes(self):
        db = self._create_database()

        self.assertEqual(db.image, 'mysqltoday')
        self.assertEqual(db.ports, '3306,22')

    @responses.activate
    def test_create_container(self):
        container = self._create_database_and_container()

        self.assertIsInstance(container, Container)

    @responses.activate
    def test_create_container_request(self):
        responses.add(responses.GET, 'http://localhost:5000/v1/containers',
            body=u'[]')

        responses.add(responses.POST, 'http://localhost:5000/v1/containers',
            body=u'{"db_port": "49154", "id": "ef458b3613b3", \
                "name": "/teal_lizard", "ssh_port": "49153", \
                "status": "running", "uri": "/v1/containers/ef458b3613b3", \
                "username": ""}',
            status=201)        

        responses.add(responses.GET, 'http://localhost:5000/v1/containers/ef458b3613b3',
            body=u'{"db_port": "49154", "id": "ef458b3613b3", \
                "name": "/teal_lizard", "ssh_port": "49153", \
                "status": "running", "uri": "/v1/containers/ef458b3613b3", \
                "username": ""}',)               

        db = self._create_database()

        self.c.get('/')

        resp = self.c.get('/databases/mysql/create', follow=True)
        self.assertEqual(resp.status_code, 200)

        self.assertIn("Your new %s database is ready!" % db, resp.content)

    @responses.activate
    def test_view_my_containers(self):
        responses.add(responses.GET, 'http://localhost:5000/v1/containers',
            body=u'[]')

        responses.add(responses.GET, 'http://localhost:5000/v1/containers/ef458b3613b3',
            body=u'{"db_port": "49154", "id": "ef458b3613b3", \
                "name": "/teal_lizard", "ssh_port": "49153", \
                "status": "running", "uri": "/v1/containers/ef458b3613b3", \
                "username": ""}',)

        self.c.get('/')
        container = self._create_database_and_container(self.c.session.session_key)

        resp = self.c.get('/databases/my-databases')

        self.assertEqual(resp.status_code, 200)
        self.assertIn(str(container), resp.content)

    def test_bad_request_return_none(self):
        self.assertEqual(get('badresource'), None)

    @responses.activate
    def test_bad_json_return_none(self):
        responses.add(responses.GET, 'http://localhost:5000/v1/containers',
            body=u'"db_port": "49154", "id": "ef458b3613b3", \
                "name": "/teal_lizard", "ssh_port": "49153", \
                "status": "running", "uri": "/v1/containers/ef458b3613b3", \
                "username": ""}',)        
        
        self.assertEqual(get('containers'), None)  

    @responses.activate
    def test_database_audit_missing_image(self):
        database = self._create_database()

        responses.add(responses.GET, 'http://localhost:5000/v1/images',
            body=u'[]')
        responses.add(responses.GET, 'http://localhost:5000/v1/containers',
            body=u'[]')
        call_command('spin_docker_audit')

        database = Database.objects.get(pk=database.id)

        self.assertFalse(database.active)

    @responses.activate
    def test_container_audit_missing_container(self):
        container = self._create_database_and_container()

        responses.add(responses.GET, 'http://localhost:5000/v1/images',
            body=u'[]')
        responses.add(responses.GET, 'http://localhost:5000/v1/containers',
            body=u'[]')        
        call_command('spin_docker_audit')

        container = Container.objects.get(pk=container.container_id)

        self.assertFalse(container.active)
