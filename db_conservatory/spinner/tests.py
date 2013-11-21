from django.test import TestCase
from django.test.client import Client
from .models import Database

class DatabaseTestCase(TestCase):
    def setUp(self):
        self.c = Client()

    def _create_database(self):
        db = Database.objects.create(name='MySQL',
            slug='mysql',
            image='mysqltoday',
            ports='3306,22')
        return db

    def test_database_attributes(self):
        self._create_database()

        db = Database.objects.get(name='MySQL')
        self.assertEqual(db.image, 'mysqltoday')
        self.assertEqual(db.ports, '3306,22')

    def test_create_container(self):
        db = self._create_database()

        container = db.create_container()
        self.assertIsInstance(container, dict)
        self.assertIn('id', container.keys())
        self.assertIn('ssh_port', container.keys())
        self.assertIn('db_port', container.keys())

    def test_create_container_request(self):
        self._create_database()

        resp = self.c.get('/databases/mysql/create', follow=True)
        self.assertEqual(resp.status_code, 200)

        self.assertIn("Your container", resp.content)
