# from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

class DatabaseTestCase(TestCase):
    def setUp(self):
        self.c = Client()

    def test_create_user_duplicate_email(self):
        data = {'first_name': 'Cornelius',
            'last_name': 'Maximus',
            'email': 'cornelius@spqr.com',
            'password1': 'rome',
            'password2': 'rome'}
        self.c.post('/register', data)

        resp = self.c.post('/register', data)

        self.assertIn('A user with that email address already exists', resp.content)

    def test_create_user_passwords_dont_match(self):
        data = {'first_name': 'Cornelius',
            'last_name': 'Maximus',
            'email': 'cornelius@spqr.com',
            'password1': 'rome',
            'password2': 'home'}
        self.c.post('/register', data)    

        resp = self.c.post('/register', data)

        self.assertIn('The two password fields didn&#39;t match.', resp.content)    
