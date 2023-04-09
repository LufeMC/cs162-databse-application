from app import create_database, session
from models.user import User
import unittest
import os

# Set up a test database
TEST_DB = "test.db"
basedir = os.path.abspath(os.path.dirname(__file__))


class TestConfig:
    """
    Testing Configuration settings for the Flask app.

    Attributes:
    - TESTING: Testing state
    - WTF_CSRF_ENABLED: Whether CSRF protection is enabled
    - DEBUG: Debug mode
    - SQLALCHEMY_DATABASE_URI: the connection URI for the database
    - LOG_FILE_NAME: Log file name
    """

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, TEST_DB)
    LOG_FILE_NAME = "log-test.txt"


class TestAuth(unittest.TestCase):
    """Test suite for the Kanban authentication routes"""

    def setUp(self):
        """Set up testing database"""
        create_database(TestConfig)

    def tearDown(self):
        """Clean up after the test"""
        pass

    def createUser(self, name, email, password, type="buyer", office_id=None):
        session.add(
            User
            ** (
                {
                    name: name,
                    email: email,
                    password: password,
                    type: type,
                    office_id: office_id,
                }
            )
        )
        session.commit()

    def getUser(self, user_id):
        user = session.query(User).filter(User.id == user_id).first()
        return user

    def test_creating_users(self):
        buyer = {"name": "buyer", "email": "buyer@example.com", "password": "password"}

        self.createUser(**buyer)
        self.assertIsNotNone(self.getUser(1))

        agent = {"name": "agent", "email": "agent@example.com", "password": "password"}

        self.createUser(**agent)
        self.assertIsNotNone(self.getUser(2))
