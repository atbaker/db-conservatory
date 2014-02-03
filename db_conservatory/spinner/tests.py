from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from .models import Database, Container
from django.core.management import call_command

import responses
import spindocker

import pdb

class DatabaseTestCase(TestCase):
    def setUp(self):
        self.c = Client()

    def _create_and_login_user(self):
        data = {'first_name': 'Cornelius',
            'last_name': 'Maximus',
            'email': 'cornelius@spqr.com',
            'password1': 'rome',
            'password2': 'rome'}
        self.c.post('/register', data)
        self.c.login(username=data['email'], password=data['password1'])

        return data['email']

    def _create_database(self):
        db = Database.objects.create(name='MySQL',
            slug='mysql',
            image='mysql',
            ports='3306,22')
        return db

    def _create_database_and_container(self, session_key=None, user=None):
        responses.add(responses.POST, 'http://localhost:8080/v1/containers',
            body=u'{"active_connections": "0", \
                "db_port": "49312", \
                "id": "de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea", \
                "image": "mysql", \
                "name": "/trusting_mccarthy", \
                "ssh_port": "49311", \
                "status": "running", \
                "uri": "/v1/containers/de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea"}',
            status=201)

        db = self._create_database()

        if user:
            user = User.objects.get(username=user)        

        if session_key == None and user == None:
            session_key = 'test'

        container = db.create_container(session_key=session_key, user=user)
        return container

    def test_database_attributes(self):
        db = self._create_database()

        self.assertEqual(db.image, 'mysql')
        self.assertEqual(db.ports, '3306,22')

    @responses.activate
    def test_create_container(self):
        container = self._create_database_and_container()

        self.assertIsInstance(container, Container)

    @responses.activate
    def test_create_container_anonymous(self):
        responses.add(responses.GET, 'http://localhost:8080/v1/containers',
            body=u'[]')

        responses.add(responses.POST, 'http://localhost:8080/v1/containers',
            body=u'{"active_connections": "0", \
                "db_port": "49312", \
                "id": "de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea", \
                "image": "mysql", \
                "name": "/trusting_mccarthy", \
                "ssh_port": "49311", \
                "status": "running", \
                "uri": "/v1/containers/de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea"}',
            status=201)        

        responses.add(responses.GET, 'http://localhost:8080/v1/containers/de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea',
            body=u'{"active_connections": "0", \
                "db_port": "49312", \
                "id": "de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea", \
                "image": "mysql", \
                "name": "/trusting_mccarthy", \
                "ssh_port": "49311", \
                "status": "running", \
                "uri": "/v1/containers/de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea"}',)               

        db = self._create_database()

        self.c.get('/')

        resp = self.c.get('/databases/mysql/create', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Your %s database is ready!" % db, resp.content)
        self.assertIn("49311", resp.content)
        self.assertIn("49312", resp.content)

        new_container = Container.objects.all()[0]
        self.assertEqual(new_container.session_key, self.c.session.session_key)
        self.assertIsNone(new_container.user)

    @responses.activate
    def test_create_container_as_user(self):
        responses.add(responses.GET, 'http://localhost:8080/v1/containers',
            body=u'[]')

        responses.add(responses.POST, 'http://localhost:8080/v1/containers',
            body=u'{"active_connections": "0", \
                "db_port": "49312", \
                "id": "de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea", \
                "image": "mysql", \
                "name": "/trusting_mccarthy", \
                "ssh_port": "49311", \
                "status": "running", \
                "uri": "/v1/containers/de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea"}',
            status=201)

        responses.add(responses.GET, 'http://localhost:8080/v1/containers/de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea',
            body=u'{"active_connections": "0", \
                "db_port": "49312", \
                "id": "de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea", \
                "image": "mysql", \
                "name": "/trusting_mccarthy", \
                "ssh_port": "49311", \
                "status": "running", \
                "uri": "/v1/containers/de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea"}')               

        db = self._create_database()

        self.c.get('/')

        user = self._create_and_login_user()

        resp = self.c.get('/databases/mysql/create', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Your %s database is ready!" % db, resp.content)  
        self.assertIn("49311", resp.content)
        self.assertIn("49312", resp.content)              

        new_container = Container.objects.all()[0]
        self.assertEqual(new_container.user.username, user)
        self.assertIsNone(new_container.session_key)

    @responses.activate
    def test_view_my_containers(self):
        responses.add(responses.GET, 'http://localhost:8080/v1/containers',
            body=u'[]')

        responses.add(responses.GET, 'http://localhost:8080/v1/containers/de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea',
            body=u'{"active_connections": "0", \
                "db_port": "49312", \
                "id": "de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea", \
                "image": "mysql", \
                "name": "/trusting_mccarthy", \
                "ssh_port": "49311", \
                "status": "running", \
                "uri": "/v1/containers/de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea"}')

        user = self._create_and_login_user()

        container = self._create_database_and_container(user=user)

        resp = self.c.get('/databases/my-databases')

        self.assertEqual(resp.status_code, 200)
        self.assertIn(str(container.name), resp.content)

    @responses.activate
    def test_bad_request_return_none(self):
        responses.add(responses.GET, 'http://localhost:8080/v1/badresource',
            status=404)

        self.assertEqual(spindocker.get('badresource'), None)

    @responses.activate
    def test_bad_json_return_none(self):
        responses.add(responses.GET, 'http://localhost:8080/v1/containers',
            body=u'"active_connections": "0", \
                "db_port": "49312", \
                "id": "de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea", \
                "image": "mysql", \
                "name": "/trusting_mccarthy", \
                "ssh_port": "49311", \
                "status": "running", \
                "uri": "/v1/containers/de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea"}',)        
        
        self.assertEqual(spindocker.get('containers'), None)  

    @responses.activate
    def test_database_audit_missing_image(self):
        database = self._create_database()

        responses.add(responses.GET, 'http://localhost:8080/v1/images',
            body=u'[]')
        responses.add(responses.GET, 'http://localhost:8080/v1/containers',
            body=u'[]')
        call_command('spin_docker_audit')

        database = Database.objects.get(pk=database.id)

        self.assertFalse(database.active)

    @responses.activate
    def test_container_audit_missing_container(self):
        container = self._create_database_and_container()

        responses.add(responses.GET, 'http://localhost:8080/v1/images',
            body=u'[]')
        responses.add(responses.GET, 'http://localhost:8080/v1/containers',
            body=u'[]')
        call_command('spin_docker_audit')

        container = Container.objects.get(pk=container.container_id)

        self.assertFalse(container.active)

    @responses.activate
    def test_stop_container(self):
        container = self._create_database_and_container()

        responses.add(responses.PATCH, 'http://localhost:8080/v1/containers/de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea',
            body=u'{"active_connections": "0", \
                "db_port": "49312", \
                "id": "de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea", \
                "image": "mysql", \
                "name": "/trusting_mccarthy", \
                "ssh_port": "49311", \
                "status": "stopping", \
                "uri": "/v1/containers/de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea"}')

        container = Container.objects.get(pk=container.container_id)
        response = container.stop()

        self.assertEqual(response['status'], 'stopping')

    @responses.activate
    def test_update_container_stop(self):
        container = self._create_database_and_container()
        user = self._create_and_login_user()

        resp = self.c.get('/databases/de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea/stop',
            follow=True)

        self.assertRedirects(resp, '/databases/my-databases', status_code=302, target_status_code=200)
        self.assertIn('is now stopped.', resp.content)

    @responses.activate
    def test_start_container(self):
        container = self._create_database_and_container()

        responses.add(responses.PATCH, 'http://localhost:8080/v1/containers/de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea',
            body=u'{"active_connections": "0", \
                "db_port": "49312", \
                "id": "de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea", \
                "image": "mysql", \
                "name": "/trusting_mccarthy", \
                "ssh_port": "49311", \
                "status": "running", \
                "uri": "/v1/containers/de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea"}')

        container = Container.objects.get(pk=container.container_id)
        response = container.start()

        self.assertEqual(response['status'], 'running')

    @responses.activate
    def test_update_container_start(self):
        container = self._create_database_and_container()

        responses.add(responses.GET, 'http://localhost:8080/v1/containers/de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea',
            body=u'{"active_connections": "0", \
                "db_port": "49312", \
                "id": "de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea", \
                "image": "mysql", \
                "name": "/trusting_mccarthy", \
                "ssh_port": "49311", \
                "status": "running", \
                "uri": "/v1/containers/de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea"}')

        resp = self.c.get('/databases/de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea/start',
            follow=True)

        self.assertRedirects(resp, '/databases/de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea', status_code=302, target_status_code=200)     

    @responses.activate
    def test_delete_container(self):
        container = self._create_database_and_container()

        responses.add(responses.DELETE, 'http://localhost:8080/v1/containers/de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea',
            body=u'[]',
            status=204)

        container = Container.objects.get(pk=container.container_id)
        response = container.delete()

        self.assertIsNone(response)
        self.assertEqual(len(Container.objects.all()), 0)   

    @responses.activate
    def test_update_container_delete(self):
        container = self._create_database_and_container()
        user = self._create_and_login_user()

        resp = self.c.get('/databases/de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea/delete',
            follow=True)

        self.assertRedirects(resp, '/databases/my-databases', status_code=302, target_status_code=200)
        self.assertIn('was deleted.', resp.content)    

    @responses.activate
    def test_view_stopped_container(self):
        container = self._create_database_and_container()
        user = self._create_and_login_user()        

        responses.add(responses.GET, 'http://localhost:8080/v1/containers/de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea',
            body=u'{"active_connections": "0", \
                "db_port": "", \
                "id": "de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea", \
                "image": "mysql", \
                "name": "/trusting_mccarthy", \
                "ssh_port": "", \
                "status": "stopped", \
                "uri": "/v1/containers/de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea"}')

        resp = self.c.get('/databases/de1288572b5131349104e9780fca8a4049a92b80a8687d6a587ae66c360906ea',
            follow=True)

        self.assertRedirects(resp, '/databases/my-databases', status_code=302, target_status_code=200)
        self.assertIn("isn't running right now.", resp.content)
