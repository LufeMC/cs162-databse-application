from faker import Faker
from werkzeug.security import generate_password_hash
from app.models.user import User
from app.extensions import db

def createBuyers(numBuyers, flaskApp):
    for i in range(numBuyers):
        fake = Faker()
        user = User(**{
            "name": fake.name(),
            "email": fake.email(),
            "password": generate_password_hash(f'buyer_password_{i}')
            })
        
        with flaskApp.app_context():
            db.session.add(user)
            db.session.commit()