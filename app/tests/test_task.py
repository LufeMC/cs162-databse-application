from app import create_app
from app.extensions import db
from app.models.task import Task
from app.models.user import User
import unittest
import os
import json

# Set up a test database
TEST_DB = 'test.db'
basedir = os.path.abspath(os.path.dirname(__file__))


class TestConfig:
    """
    Testing Configuration settings for the Flask app.

    Attributes:
    - TESTING: Testing state
    - WTF_CSRF_ENABLED: Whether CSRF protection is enabled
    - DEBUG: Debug mode
    - SQLALCHEMY_DATABASE_URI: the connection URI for the database
    """
    TESTING = True
    WTF_CSRF_ENABLED = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, TEST_DB)


class TestTasks(unittest.TestCase):
    """Test suite for the Kanban task management routes"""

    def setUp(self):
        """Set up Kanban app, database, and test client"""
        self.flaskApp = create_app(TestConfig)
        self.app = self.flaskApp.test_client()

        with self.flaskApp.app_context():
            db.drop_all()
            db.create_all()

        self.assertEqual(self.flaskApp.debug, False)

    def tearDown(self):
        """Clean up after the test"""
        pass

    def register(self, firstName, lastName, email, password):
        """
        Test helper function that sends a POST request to the '/auth/register' route.

        Args:
            firstName (str): The first name of the user to register
            lastName (str): The last name of the user to register
            email (str): The email address of the user to register
            password (str): The password of the user to register

        Returns:
            The response object of the POST request
        """
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
        """
        Test helper function that sends a POST request to the '/auth/login' route.

        Args:
            email (str): The email address of the user to log in
            password (str): The password of the user to log in

        Returns:
            The response object of the POST request
        """
        return self.app.post(
            '/auth/login',
            data=json.dumps({"email": email, "password": password}),
            follow_redirects=True,
            headers={
                "Content-Type": "application/json"
            }
        )

    def add_task(self, name, description):
        """Simulates a request to add a new task to the Flask app

        Args:
            name (str): The name of the task
            description (str): The description of the task

        Returns:
            The response object returned by the Flask app
        """
        return self.app.post(
            '/home/add',
            data=json.dumps({"name": name, "description": description}),
            follow_redirects=True,
            headers={
                "Content-Type": "application/json"
            }
        )

    def next_task(self, uuid):
        """Simulates a request to move a task to the next step in the Flask app

        Args:
            uuid (str): The UUID of the task to move to the next step

        Returns:
            The response object returned by the Flask app
        """
        return self.app.patch(
            '/home/move/next',
            data=json.dumps({"uuid": uuid}),
            follow_redirects=True,
            headers={
                "Content-Type": "application/json"
            }
        )

    def previous_task(self, uuid):
        """
        Send a request to move a task to the previous status.

        Args:
            uuid (str): The UUID of the task to be moved.

        Returns:
            The Flask response to the request to move the task.
        """
        return self.app.patch(
            '/home/move/previous',
            data=json.dumps({"uuid": uuid}),
            follow_redirects=True,
            headers={
                "Content-Type": "application/json"
            }
        )

    def delete_task(self, uuid):
        """
        Deletes a task with a given UUID.

        Args:
            uuid (str): The UUID of the task to delete.

        Returns:
            The response object for the DELETE request to delete the task.
        """
        return self.app.delete(
            f'/home/remove/{uuid}',
            follow_redirects=True,
            headers={
                "Content-Type": "application/json"
            }
        )

    def test_auth(self):
        """
        Test the task management routes.

        This method performs the following tests:
        - Test that registering a user with a unique email address works.
        - Test that logging in with a valid email address and password works.
        - Tests that creating a new task works
        - Tests that moving a task to the next step works
        - Tests that moving a task to the previous step works
        - Tests that deleting a task works
        """

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
