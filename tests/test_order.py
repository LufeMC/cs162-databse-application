from app import create_database
from tests.test_extensions import session
from extensions import info_logger, error_logger
from models.listing import Listing
from models.user import User
from models.order import Order
import unittest
from tests.test_config import TestConfig


class TestOrder(unittest.TestCase):
    """Test suite for adding orders to the database"""

    def setUp(self):
        """Set up testing database"""
        self.tearDown()
        print("\n\n=== Creating order creation ===\n")
        create_database(TestConfig)

    def tearDown(self):
        """Clean up after the test"""
        for handler in info_logger.handlers:
            info_logger.removeHandler(handler)
            handler.close()
        for handler in error_logger.handlers:
            error_logger.removeHandler(handler)
            handler.close()

    def createListing(self, name, num_bedrooms, num_bathrooms, garage, price, zip_code):
        newListing = Listing(
            **{
                "name": name,
                "num_bedrooms": num_bedrooms,
                "num_bathrooms": num_bathrooms,
                "garage": garage,
                "price": price,
                "zip_code": zip_code,
            }
        )

        session.add(newListing)
        session.commit()

        return newListing

    def getListing(self, listing_id):
        listing = session.query(Listing).filter(Listing.id == listing_id).first()
        return listing

    def createUser(self, name, email, password, type="buyer", office_id=None):
        newUser = User(
            **{
                "name": name,
                "email": email,
                "password": password,
                "type": type,
                "office_id": office_id,
            }
        )
        session.add(newUser)
        session.commit()

        return newUser

    def getUser(self, user_id):
        user = session.query(User).filter(User.id == user_id).first()
        return user

    def createOrder(self, listing_id, buyer_id, agent_id):
        order = Order(
            listing_id=listing_id,
            buyer_id=buyer_id,
            agent_id=agent_id,
        )
        session.add(order)
        session.commit()

    def test_creating_order(self):
        # create test listing and users
        listing = {
            "name": "Test Listing",
            "num_bedrooms": 2,
            "num_bathrooms": 2,
            "garage": True,
            "price": 500000,
            "zip_code": "12345",
        }
        buyer = {
            "email": "testbuyer@test.com",
            "password": "password",
            "name": "Test Buyer",
        }
        agent = {
            "email": "testagent@test.com",
            "password": "password",
            "name": "Test Agent",
            "type": "agent",
        }

        listing = self.createListing(**listing)
        buyer = self.createUser(**buyer)
        agent = self.createUser(**agent)

        # create order with the test listing and users
        self.createOrder(listing.id, buyer.id, agent.id)

        # check that the order was created correctly
        order = session.query(Order).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.listing_id, listing.id)
        self.assertEqual(order.buyer_id, buyer.id)
        self.assertEqual(order.agent_id, agent.id)

    def test_repr(self):
        # create test order
        order = Order(listing_id=1, buyer_id=1, agent_id=2)
        session.add(order)
        session.commit()

        # check that the repr method returns the expected string
        expected_string = f'<Order "{order.id}">'
        self.assertEqual(str(order), expected_string)
