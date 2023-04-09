from app import create_database
from tests.test_extensions import session
from extensions import info_logger, error_logger
from models.user import User
import unittest
from tests.test_config import TestConfig


class TestUser(unittest.TestCase):
    """Test suite for the Kanban authentication routes"""

    def setUp(self):
        """Set up testing database"""
        self.tearDown()
        print("\n\n=== Creating user creation ===\n")
        create_database(TestConfig)

    def tearDown(self):
        """Clean up after the test"""
        for handler in info_logger.handlers:
            info_logger.removeHandler(handler)
            handler.close()
        for handler in error_logger.handlers:
            error_logger.removeHandler(handler)
            handler.close()

    def createUser(self, name, email, password, type="buyer", office_id=None):
        session.add(
            User(
                **{
                    "name": name,
                    "email": email,
                    "password": password,
                    "type": type,
                    "office_id": office_id,
                }
            )
        )
        session.commit()

    def getUser(self, user_id):
        user = session.query(User).filter(User.id == user_id).first()
        return user

    def test_creating_buyer(self):
        buyer = {"name": "buyer", "email": "buyer@example.com", "password": "password"}

        self.createUser(**buyer)

        buyer = self.getUser(1)

        self.assertIsNotNone(buyer)
        self.assertEqual(buyer.name, "buyer")
        self.assertEqual(buyer.email, "buyer@example.com")

    def test_creating_agent(self):
        agent = {
            "name": "agent",
            "email": "agent@example.com",
            "password": "password",
            "type": "agent",
        }

        self.createUser(**agent)

        agent = self.getUser(1)

        self.assertIsNotNone(agent)
        self.assertEqual(agent.name, "agent")
        self.assertEqual(agent.email, "agent@example.com")
        self.assertEqual(agent.type, "agent")

    def test_get_user_by_nonexistent_id(self):
        user = self.getUser(1)

        self.assertIsNone(user)

    def test_updating_user(self):
        user = {"name": "John", "email": "john@example.com", "password": "password"}
        self.createUser(**user)

        user_id = 1
        new_name = "Jane"
        new_email = "jane@example.com"
        session.query(User).filter(User.id == user_id).update(
            {"name": new_name, "email": new_email}
        )
        session.commit()

        user = self.getUser(user_id)
        self.assertEqual(user.name, new_name)
        self.assertEqual(user.email, new_email)

    def test_deleting_user(self):
        user = {"name": "John", "email": "john@example.com", "password": "password"}
        self.createUser(**user)

        user_id = 1
        session.query(User).filter(User.id == user_id).delete()
        session.commit()

        user = self.getUser(user_id)
        self.assertIsNone(user)
