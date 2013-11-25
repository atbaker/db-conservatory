from django.test import TestCase
from django.test.client import Client
from .models import Database, Container

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
        db = self._create_database()
        container = db.create_container(session_key)
        return container

    def test_database_attributes(self):
        db = self._create_database()

        self.assertEqual(db.image, 'mysqltoday')
        self.assertEqual(db.ports, '3306,22')

    def test_create_container(self):
        container = self._create_database_and_container()

        self.assertIsInstance(container, Container)

    def test_create_container_request(self):
        db = self._create_database()

        self.c.get('/')

        resp = self.c.get('/databases/mysql/create', follow=True)
        self.assertEqual(resp.status_code, 200)

        self.assertIn("Your new %s database is ready!" % db, resp.content)

    def test_view_my_containers(self):
        self.c.get('/')
        container = self._create_database_and_container(self.c.session.session_key)

        resp = self.c.get('/databases/my-databases')

        self.assertEqual(resp.status_code, 200)
        self.assertIn(str(container), resp.content)
