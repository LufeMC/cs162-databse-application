from app import create_database
from tests.test_extensions import session
from extensions import info_logger, error_logger
from models.user import User
from models.listing import Listing
from models.order import Order
from models.office import Office
from models.commission import Commission
import unittest
from tests.test_config import TestConfig
from fakeData.createRates import createRates
from query import (
    get_top_5_offices_month,
    get_top_5_agents_month,
    get_averages,
    create_commissions,
)
from datetime import datetime, timedelta
import calendar


class TestQueries(unittest.TestCase):
    """Test suite for the queries"""

    def setUp(self):
        """Set up testing database and create tables"""
        self.tearDown()
        print("\n\n=== Creating queries ===\n")
        create_database(TestConfig)

    def tearDown(self):
        """Remove handlers and close them to avoid memory leaks"""
        for handler in info_logger.handlers:
            info_logger.removeHandler(handler)
            handler.close()
        for handler in error_logger.handlers:
            error_logger.removeHandler(handler)
            handler.close()

    def createUser(self, name, email, password, type="buyer", office_id=None):
        """Create a new user.

        Args:
            name (str): Name of the user.
            email (str): Email of the user.
            password (str): Password of the user.
            type (str, optional): Type of user. Defaults to "buyer".
            office_id (int, optional): Id of the office the user belongs to. Defaults to None.
        """
        # Create a new user and commit changes to the session
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
        """Retrieve a user by id.

        Args:
            user_id (int): Id of the user.

        Returns:
            User: The user object.
        """
        # Query the session to retrieve a user by id
        user = session.query(User).filter(User.id == user_id).first()
        return user

    def createListing(self, name, num_bedrooms, num_bathrooms, garage, price, zip_code):
        """Create a new listing.

        Args:
            name (str): Name of the listing.
            num_bedrooms (int): Number of bedrooms in the listing.
            num_bathrooms (int): Number of bathrooms in the listing.
            garage (bool): True if the listing has a garage, False otherwise.
            price (float): Price of the listing.
            zip_code (str): Zip code of the listing.

        Returns:
            Listing: The newly created listing object.
        """
        # Create a new listing and commit changes to the session
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
        """Retrieve a listing by id.

        Args:
            listing_id (int): Id of the listing.

        Returns:
            Listing: The listing object.
        """
        # Query the session to retrieve a listing by id
        listing = session.query(Listing).filter(Listing.id == listing_id).first()
        return listing

    def createOrder(self, listing_id, buyer_id, agent_id):
        """Create a new order.

        Args:
            listing_id (int): Id of the listing.
            buyer_id (int): Id of the buyer.
            agent_id (int): Id of the agent.

        Returns:
            None
        """
        date_sold = datetime.now()
        order = Order(
            listing_id=listing_id,
            buyer_id=buyer_id,
            agent_id=agent_id,
            date_created=date_sold,
        )
        listing = session.query(Listing).filter(Listing.id == listing_id).first()
        listing.sold = True
        listing.date_sold = date_sold
        session.add(order)
        session.commit()

    def getOrder(self, order_id):
        """Retrieve a order by id.

        Args:
            order_id (int): Id of the order.

        Returns:
            Order: The order object.
        """
        order = session.query(Order).filter(Order.id == order_id).first()
        return order

    def createOffice(self, name):
        """Create a new office.

        Args:
            name (int): Name of the office.

        Returns:
            None
        """
        session.add(
            Office(
                **{
                    "name": name,
                }
            )
        )
        session.commit()

    def getOffice(self, office_id, agents):
        """Retrieve a office by id.

        Args:
            office_id (int): Id of the office.
            agents (bool): Whether the office has agents or not.

        Returns:
            Office: The office object.
        """
        if agents:
            office = (
                session.query(Office).join(User).filter(Office.id == office_id).first()
            )
        else:
            office = session.query(Office).filter(Office.id == office_id).first()

        return office

    def getCommission(self, agent_id):
        """Retrieve a commission by agent id.

        Args:
            agent_id (int): Id of the commission.

        Returns:
            Commission: The commission object.
        """
        commission = (
            session.query(Commission).filter(Commission.agent_id == agent_id).first()
        )

        return commission

    def createFakeData(self):
        """Creates the fake data in the database

        Args:

        Returns:
            None
        """

        # Creates default rates
        createRates(session)

        for i in range(10):
            buyer = {
                "name": f"buyer {i + 1}",
                "email": f"buyer{i + 1}@example.com",
                "password": "password",
            }

            self.createUser(**buyer)

        for i in range(6):
            office = {
                "name": f"office {i + 1}",
            }

            self.createOffice(**office)

        for i in range(10, 16):
            agent = {
                "name": f"agent {i - 9}",
                "email": f"agent{i - 9}@example.com",
                "password": "password",
                "type": "agent",
                "office_id": i - 9,
            }

            self.createUser(**agent)

        for i in range(30):
            listing = {
                "name": f"listing {i + 1}",
                "num_bedrooms": 1,
                "num_bathrooms": 1,
                "garage": True,
                "price": 100000,
                "zip_code": "10000",
            }

            self.createListing(**listing)

        self.createOrder(1, 1, 11)
        self.createOrder(2, 1, 11)
        self.createOrder(3, 1, 11)
        self.createOrder(4, 1, 11)
        self.createOrder(5, 1, 11)
        self.createOrder(6, 1, 11)
        self.createOrder(7, 2, 12)
        self.createOrder(8, 2, 12)
        self.createOrder(9, 2, 12)
        self.createOrder(10, 2, 12)
        self.createOrder(11, 2, 12)
        self.createOrder(12, 3, 13)
        self.createOrder(13, 3, 13)
        self.createOrder(14, 3, 13)
        self.createOrder(15, 3, 13)
        self.createOrder(16, 4, 14)
        self.createOrder(17, 4, 14)
        self.createOrder(18, 4, 14)
        self.createOrder(19, 5, 15)
        self.createOrder(20, 5, 15)
        self.createOrder(21, 6, 16)

    def test_top_5_offices(self):
        self.createFakeData()

        date_datetime = datetime.now()
        first_day_of_current_month = datetime(
            date_datetime.year, date_datetime.month, 1
        )
        last_day_of_current_month = first_day_of_current_month.replace(
            day=calendar.monthrange(
                first_day_of_current_month.year, first_day_of_current_month.month
            )[1]
        )
        last_second_of_current_month = (
            last_day_of_current_month + timedelta(days=1) - timedelta(seconds=1)
        )

        top_5_offices_month = get_top_5_offices_month(
            first_day_of_current_month, last_second_of_current_month, session
        )

        self.assertEqual(top_5_offices_month[0][0].id, 1)
        self.assertEqual(top_5_offices_month[0][1], 6)

        self.assertEqual(top_5_offices_month[1][0].id, 2)
        self.assertEqual(top_5_offices_month[1][1], 5)

        self.assertEqual(top_5_offices_month[2][0].id, 3)
        self.assertEqual(top_5_offices_month[2][1], 4)

        self.assertEqual(top_5_offices_month[3][0].id, 4)
        self.assertEqual(top_5_offices_month[3][1], 3)

        self.assertEqual(top_5_offices_month[4][0].id, 5)
        self.assertEqual(top_5_offices_month[4][1], 2)

    def test_top_5_agents(self):
        self.createFakeData()

        date_datetime = datetime.now()
        first_day_of_current_month = datetime(
            date_datetime.year, date_datetime.month, 1
        )
        last_day_of_current_month = first_day_of_current_month.replace(
            day=calendar.monthrange(
                first_day_of_current_month.year, first_day_of_current_month.month
            )[1]
        )
        last_second_of_current_month = (
            last_day_of_current_month + timedelta(days=1) - timedelta(seconds=1)
        )

        top_5_agents_month = get_top_5_agents_month(
            first_day_of_current_month, last_second_of_current_month, session
        )

        self.assertEqual(top_5_agents_month[0][0].id, 11)
        self.assertEqual(top_5_agents_month[0][1], 6)

        self.assertEqual(top_5_agents_month[1][0].id, 12)
        self.assertEqual(top_5_agents_month[1][1], 5)

        self.assertEqual(top_5_agents_month[2][0].id, 13)
        self.assertEqual(top_5_agents_month[2][1], 4)

        self.assertEqual(top_5_agents_month[3][0].id, 14)
        self.assertEqual(top_5_agents_month[3][1], 3)

        self.assertEqual(top_5_agents_month[4][0].id, 15)
        self.assertEqual(top_5_agents_month[4][1], 2)

    def test_average_days_on_market(self):
        self.createFakeData()

        date_datetime = datetime.now()
        first_day_of_current_month = datetime(
            date_datetime.year, date_datetime.month, 1
        )
        last_day_of_current_month = first_day_of_current_month.replace(
            day=calendar.monthrange(
                first_day_of_current_month.year, first_day_of_current_month.month
            )[1]
        )
        last_second_of_current_month = (
            last_day_of_current_month + timedelta(days=1) - timedelta(seconds=1)
        )

        averages = get_averages(
            first_day_of_current_month, last_second_of_current_month, session
        )

        self.assertEqual(averages[1], 0)

    def test_average_price(self):
        self.createFakeData()

        date_datetime = datetime.now()
        first_day_of_current_month = datetime(
            date_datetime.year, date_datetime.month, 1
        )
        last_day_of_current_month = first_day_of_current_month.replace(
            day=calendar.monthrange(
                first_day_of_current_month.year, first_day_of_current_month.month
            )[1]
        )
        last_second_of_current_month = (
            last_day_of_current_month + timedelta(days=1) - timedelta(seconds=1)
        )

        averages = get_averages(
            first_day_of_current_month, last_second_of_current_month, session
        )

        self.assertEqual(averages[0], 100000)

    def test_commission(self):
        self.createFakeData()

        date_datetime = datetime.now()
        first_day_of_current_month = datetime(
            date_datetime.year, date_datetime.month, 1
        )
        last_day_of_current_month = first_day_of_current_month.replace(
            day=calendar.monthrange(
                first_day_of_current_month.year, first_day_of_current_month.month
            )[1]
        )
        last_second_of_current_month = (
            last_day_of_current_month + timedelta(days=1) - timedelta(seconds=1)
        )

        create_commissions(
            first_day_of_current_month, last_second_of_current_month, session
        )

        agent_1_commission = self.getCommission(11)
        self.assertEqual(agent_1_commission.total_commission, 45000)

        agent_2_commission = self.getCommission(12)
        self.assertEqual(agent_2_commission.total_commission, 37500)

        agent_3_commission = self.getCommission(13)
        self.assertEqual(agent_3_commission.total_commission, 30000)

        agent_4_commission = self.getCommission(14)
        self.assertEqual(agent_4_commission.total_commission, 22500)

        agent_5_commission = self.getCommission(15)
        self.assertEqual(agent_5_commission.total_commission, 15000)

        agent_6_commission = self.getCommission(16)
        self.assertEqual(agent_6_commission.total_commission, 7500)
