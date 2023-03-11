from app import create_app
from app.extensions import db
from app.models.task import Task
from app.models.user import User
import unittest
import os
import json

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

    def register(self, firstName, lastName, email, password):
        return self.app.post(
            '/auth/register',
            data=json.dumps({"firstName": firstName, "lastName": lastName,
                             "email": email, "password": password}),
            follow_redirects=True,
            headers={
                "Content-Type": "application/json"
            }
        )

    def login(self, email, password):
        return self.app.post(
            '/auth/login',
            data=json.dumps({"email": email, "password": password}),
            follow_redirects=True,
            headers={
                "Content-Type": "application/json"
            }
        )

    def add_task(self, name, description):
        return self.app.post(
            '/home/add',
            data=json.dumps({"name": name, "description": description}),
            follow_redirects=True,
            headers={
                "Content-Type": "application/json"
            }
        )

    def next_task(self, uuid):
        return self.app.patch(
            '/home/move/next',
            data=json.dumps({"uuid": uuid}),
            follow_redirects=True,
            headers={
                "Content-Type": "application/json"
            }
        )

    def previous_task(self, uuid):
        return self.app.patch(
            '/home/move/previous',
            data=json.dumps({"uuid": uuid}),
            follow_redirects=True,
            headers={
                "Content-Type": "application/json"
            }
        )

    def delete_task(self, uuid):
        return self.app.delete(
            f'/home/remove/{uuid}',
            follow_redirects=True,
            headers={
                "Content-Type": "application/json"
            }
        )

    def test_auth(self):
        # Register new user
        registerResponse = self.register(
            'TestFirst', 'TestLast', 'test@test.com', '123456')
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

        # Checking if task moved to next
        with self.flaskApp.app_context():
            newTask = Task.query.one()

        self.assertEqual(newTask.status, 1)

        # Moving task to previous step
        taskNextResponse = self.previous_task(newTask.uuid)
        self.assertEqual(taskNextResponse.status_code, 204)

        # Checking if task moved to previous
        with self.flaskApp.app_context():
            newTask = Task.query.one()

        self.assertEqual(newTask.status, 0)

        # Deleting task
        taskNextResponse = self.delete_task(newTask.uuid)
        self.assertEqual(taskNextResponse.status_code, 204)

        # Checking if task is deleted
        with self.flaskApp.app_context():
            newTask = Task.query.first()

        self.assertEqual(newTask.deleted, True)
