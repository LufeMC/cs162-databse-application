from app import create_database
from tests.test_extensions import session
from extensions import info_logger, error_logger
from models.listing import Listing
import unittest
from tests.test_config import TestConfig
import datetime


class TestListing(unittest.TestCase):
    """Test suite for the Kanban authentication routes"""

    def setUp(self):
        """Set up testing database"""
        self.tearDown()
        print("\n\n=== Creating listing creation ===\n")
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
        session.add(
            Listing(
                **{
                    "name": name,
                    "num_bedrooms": num_bedrooms,
                    "num_bathrooms": num_bathrooms,
                    "garage": garage,
                    "price": price,
                    "zip_code": zip_code,
                }
            )
        )
        session.commit()

    def getListing(self, listing_id):
        listing = session.query(Listing).filter(Listing.id == listing_id).first()
        return listing

    def test_creating_listing(self):
        listing = {
            "name": "listing 1",
            "num_bedrooms": 1,
            "num_bathrooms": 1,
            "garage": True,
            "price": 250000,
            "zip_code": "10000",
        }

        self.createListing(**listing)

        listing = self.getListing(1)

        self.assertIsNotNone(listing)
        self.assertEqual(listing.name, "listing 1")
        self.assertEqual(listing.num_bedrooms, 1)
        self.assertEqual(listing.num_bathrooms, 1)
        self.assertTrue(listing.garage)
        self.assertEqual(listing.price, 250000)
        self.assertEqual(listing.zip_code, "10000")

    def test_updating_listing(self):
        listing = {
            "name": "listing 1",
            "num_bedrooms": 1,
            "num_bathrooms": 1,
            "garage": True,
            "price": 250000,
            "zip_code": "10000",
        }

        # create the listing
        self.createListing(**listing)

        # update the listing
        updated_listing = {
            "name": "listing 1 updated",
            "num_bedrooms": 2,
            "num_bathrooms": 2,
            "garage": False,
            "price": 300000,
            "zip_code": "20000",
        }

        listing_to_update = self.getListing(1)
        listing_to_update.name = updated_listing["name"]
        listing_to_update.num_bedrooms = updated_listing["num_bedrooms"]
        listing_to_update.num_bathrooms = updated_listing["num_bathrooms"]
        listing_to_update.garage = updated_listing["garage"]
        listing_to_update.price = updated_listing["price"]
        listing_to_update.zip_code = updated_listing["zip_code"]
        session.commit()

        # check that the listing was updated correctly
        updated_listing = self.getListing(1)
        self.assertEqual(updated_listing.name, "listing 1 updated")
        self.assertEqual(updated_listing.num_bedrooms, 2)
        self.assertEqual(updated_listing.num_bathrooms, 2)
        self.assertFalse(updated_listing.garage)
        self.assertEqual(updated_listing.price, 300000)
        self.assertEqual(updated_listing.zip_code, "20000")

    def test_listing_sold(self):
        listing = {
            "name": "listing 1",
            "num_bedrooms": 1,
            "num_bathrooms": 1,
            "garage": True,
            "price": 250000,
            "zip_code": "10000",
        }

        # create the listing
        self.createListing(**listing)

        # mark the listing as sold
        listing_to_sell = self.getListing(1)
        listing_to_sell.sold = True
        listing_to_sell.date_sold = datetime.datetime.utcnow()
        session.commit()

        # check that the listing is marked as sold
        sold_listing = self.getListing(1)
        self.assertTrue(sold_listing.sold)
        self.assertIsNotNone(sold_listing.date_sold)

    def test_listing_deleted(self):
        listing = {
            "name": "listing 1",
            "num_bedrooms": 1,
            "num_bathrooms": 1,
            "garage": True,
            "price": 250000,
            "zip_code": "10000",
        }

        # create the listing
        self.createListing(**listing)

        # delete the listing
        listing_to_delete = self.getListing(1)
        session.delete(listing_to_delete)
        session.commit()

        # check that the listing was deleted
        deleted_listing = self.getListing(1)
        self.assertIsNone(deleted_listing)
