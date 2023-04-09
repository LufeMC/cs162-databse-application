from faker import Faker
from models.listing import Listing
from extensions import session, info_logger, error_logger
import random
import datetime


def createListings(numListings):
    """
    Create a given number of fake listings with random names, number of bedrooms,
    number of bethrooms, garages, prices and zip codes.
    The created listings will be added to the session and committed to the database.

    Args:
        numListings (int): Number of listings to create.

    Returns:
        None
    """
    try:
        for _ in range(numListings):
            fake = Faker()
            listing = Listing(
                **{
                    "name": fake.street_name(),
                    "num_bedrooms": int(random.randint(1, 4)),
                    "num_bethrooms": int(random.randint(1, 4)),
                    "garage": fake.pybool(),
                    "price": round(random.uniform(50000, 2000000), 2),
                    "zip_code": fake.postcode(),
                    "sold": False,
                    "date_created": fake.date_between(datetime.date(2023, 1, 1)),
                }
            )

            session.add(listing)

        session.commit()
        info_logger.info("Listings data created")
    except Exception as error:
        error_logger.error(f'"{error}" -> Error on creating listings data')
