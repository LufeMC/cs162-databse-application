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

    def add_task(self, name, description):
        return self.app.post(
            '/home/add',
            data=dict(name=name, description=description),
            follow_redirects=True
        )

    def next_task(self, uuid):
        return self.app.post(
            '/home/next',
            data=dict(uuid=uuid),
            follow_redirects=True
        )

    def previous_task(self, uuid):
        return self.app.post(
            '/home/previous',
            data=dict(uuid=uuid),
            follow_redirects=True
        )

    def delete_task(self, uuid):
        return self.app.post(
            '/home/delete',
            data=dict(uuid=uuid),
            follow_redirects=True
        )

    def test_auth(self):
        # Register new user
        registerResponse = self.register('test@test.com', '123456')
        self.assertEqual(registerResponse.status_code, 201)

        # Logging into account
        loginResponse = self.login('test@test.com', '123456')
        self.assertEqual(loginResponse.status_code, 200)

        # Creating a new task
        newTaskResponse = self.add_task(
            'Testing task', 'This is a testing task')
        self.assertEqual(newTaskResponse.status_code, 201)

        with self.flaskApp.app_context():
            newTask = Task.query.one()

        # Moving task to next step
        taskNextResponse = self.next_task(newTask.uuid)
        self.assertEqual(taskNextResponse.status_code, 204)

        # Moving task to previous step
        taskNextResponse = self.previous_task(newTask.uuid)
        self.assertEqual(taskNextResponse.status_code, 204)

        # Deleting task
        taskNextResponse = self.delete_task(newTask.uuid)
        self.assertEqual(taskNextResponse.status_code, 204)
