from faker import Faker
from werkzeug.security import generate_password_hash
from app.models.office import Office
from app.extensions import db

def createOffices(numOffices, flaskApp):
    for _ in range(numOffices):
        fake = Faker()
        office = Office(**{
            "name": fake.company(),
            })
        
        with flaskApp.app_context():
            db.session.add(office)
            db.session.commit()