from faker import Faker
from werkzeug.security import generate_password_hash
from app.models.user import User
from app.extensions import db
import random

def createAgents(numBuyers, numOffices, flaskApp):
    for i in range(numBuyers):
        fake = Faker()
        user = User(**{
            "name": fake.name(),
            "email": fake.email(),
            "password": generate_password_hash(f'buyer_password_{i}'),
            "type": "agent",
            "office_id": random.choice([i + 1 for i in range(numOffices)])
            })
        
        with flaskApp.app_context():
            db.session.add(user)
            db.session.commit()