from flask import request
from flask_language import current_language

from base import BaseTestCase

class TestLogin(BaseTestCase):

    # Ensure user can access the login page
    def test_login_route(self):
        response = self.client.get('/login')
        self.assertInResponseWithLang('LOGIN', response)
        self.assertInResponseWithLang('USERNAME', response)
        self.assertInResponseWithLang('PASSWORD', response)

    # Ensure user can login
    def test_login(self):
        # Student login
        response = self.client.post('/login', data=dict(
                username='teststudent1', password='12345678'
            ), follow_redirects=True)
        self.assertIn(b'Hi', response.data)

        # Lecturer login
        response = self.client.post('/login', data=dict(
                username='testlecturer1', password='12345678'
            ), follow_redirects=True)
        self.assertIn(b'Hi', response.data)

        # Course designer login
        response = self.client.post('/login', data=dict(
                username='testcd1', password='12345678'
            ), follow_redirects=True)
        self.assertIn(b'Hi', response.data)

    def test_login_invalid_username(self):
        response = self.client.post('/login', data=dict(
                username='voiduser', password='12345678'
            ), follow_redirects=True)
        self.assertInResponseWithLang('INVALID_CREDENTIALS', response)

    def test_login_invalid_password(self):
        response = self.client.post('/login', data=dict(
                username='teststudent1', password='awrongpassword'
            ), follow_redirects=True)
        self.assertInResponseWithLang('INVALID_CREDENTIALS', response)

    
