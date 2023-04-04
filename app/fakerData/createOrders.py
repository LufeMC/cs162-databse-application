from faker import Faker
from werkzeug.security import generate_password_hash
from app.models.order import Order
from app.models.listing import Listing
from app.extensions import db
import random
import datetime

def createOrders(numOrders, numListings, numAgents, numBuyers, flaskApp):
    idsChosen = set()
    for _ in range(int(numOrders)):
        fake = Faker()
        listing_id = random.choice([i + 1 for i in range(numListings)])

        while listing_id in idsChosen:
            listing_id = random.choice([i + 1 for i in range(numListings)])
        
        idsChosen.add(listing_id)

        with flaskApp.app_context():
            listing = Listing.query.filter_by(id = listing_id).first()
            date_sold = listing.date_created + datetime.timedelta(days = random.randint(1,50))
            if (date_sold > datetime.datetime.now()):
                date_sold = datetime.datetime.now()
                
            listing.date_sold = date_sold
            listing.sold = True
            db.session.commit()

        order = Order(**{
            "listing_id": listing_id,
            "agent_id": random.choice([i + 1 for i in range(numAgents)]),
            "buyer_id": random.choice([i + 1 for i in range(numBuyers)]),
            })
        
        with flaskApp.app_context():
            db.session.add(order)
            db.session.commit()