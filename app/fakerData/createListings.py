from faker import Faker
from werkzeug.security import generate_password_hash
from app.models.listing import Listing
from app.extensions import db
import random
import datetime

def createListings(numListings, flaskApp):
    for _ in range(numListings):
        fake = Faker()
        listing = Listing(**{
            "name": fake.street_name(),
            "num_bedrooms": int(random.randint(1,4)),
            "num_bethrooms": int(random.randint(1,4)),
            "garage": fake.pybool(),
            "price": round(random.uniform(50000, 2000000), 2),
            "zip_code": fake.postcode(),
            "sold": False,
            "date_created": fake.date_between(datetime.date(2021,1,1))
            })
        
        with flaskApp.app_context():
            db.session.add(listing)
            db.session.commit()