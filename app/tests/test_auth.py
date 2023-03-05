from app import create_app
from app.extensions import db
from app.models.task import Task
from app.models.user import User
import unittest
import os

TEST_DB = 'test.db'
basedir = os.path.abspath(os.path.dirname(__file__))


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.flaskApp = create_app()
        self.flaskApp.config['TESTING'] = True
        self.flaskApp.config['WTF_CSRF_ENABLED'] = False
        self.flaskApp.config['DEBUG'] = False
        self.flaskApp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = self.flaskApp.test_client()

        with self.flaskApp.app_context():
            db.drop_all()
            db.create_all()

        self.assertEqual(self.flaskApp.debug, False)

    def tearDown(self):
        pass

    def register(self, email, password):
        return self.app.post(
            '/auth/register',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def login(self, email, password):
        return self.app.post(
            '/auth/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def test_auth(self):
        # Check if routes return 200
        response = self.app.get('/auth/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.app.get('/auth/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check if registering works
        registerResponse = self.register('test@test.com', '123456')
        self.assertEqual(registerResponse.status_code, 201)

        # Check if registering doesn't work in case email is already registered
        registerResponse = self.register('test@test.com', '123456')
        self.assertEqual(registerResponse.status_code, 202)

        # Check if login works
        loginResponse = self.login('test@test.com', '123456')
        self.assertEqual(loginResponse.status_code, 200)

        # Check if login doesn't work with wrong password
        loginResponse = self.login('test@test.com', '12345')
        self.assertEqual(loginResponse.status_code, 401)

        # Check if login doesn't work with unexistent account
        loginResponse = self.login('test_unexistent@test.com', '123456')
        self.assertEqual(loginResponse.status_code, 404)
