from app import create_database
from tests.test_extensions import session
from extensions import info_logger, error_logger
from models.user import User
from models.office import Office
import unittest
from tests.test_config import TestConfig


class TestOffice(unittest.TestCase):
    """Test suite for the Kanban authentication routes"""

    def setUp(self):
        """Set up testing database"""
        self.tearDown()
        print("\n\n=== Creating office with agent ===\n")
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

    def createOffice(self, name):
        session.add(
            Office(
                **{
                    "name": name,
                }
            )
        )
        session.commit()

    def getOffice(self, office_id, agents):
        if agents:
            office = (
                session.query(Office).join(User).filter(Office.id == office_id).first()
            )
        else:
            office = session.query(Office).filter(Office.id == office_id).first()

        return office

    def test_create_office(self):
        # Test creating an office
        office = {"name": "office"}

        self.createOffice(**office)

        office = self.getOffice(1, False)

        self.assertIsNotNone(office)
        self.assertEqual(office.name, "office")

    def test_create_agent(self):
        # Test creating an agent
        agent = {
            "name": "agent",
            "email": "agent@example.com",
            "password": "password",
            "type": "agent",
            "office_id": 1,
        }

        self.createUser(**agent)

        agent = self.getUser(1)

        self.assertIsNotNone(agent)
        self.assertEqual(agent.name, "agent")
        self.assertEqual(agent.email, "agent@example.com")
        self.assertEqual(agent.type, "agent")

    def test_add_agent_to_office(self):
        # Test adding an agent to an office
        self.createOffice(name="office")

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

        office = self.getOffice(1, False)
        self.assertEqual(len(office.agents), 0)

        agent.office_id = 1
        session.commit()

        office = self.getOffice(1, True)
        self.assertEqual(len(office.agents), 1)
        self.assertEqual(office.agents[0].id, 1)
        self.assertEqual(office.agents[0].name, "agent")

    def test_repr(self):
        # Test __repr__() method
        self.createOffice(name="office")

        office = self.getOffice(1, False)
        self.assertEqual(repr(office), '<Office "office">')
