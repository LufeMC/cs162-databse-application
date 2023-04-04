from app.extensions import db
import datetime


class Listing(db.Model):
    """
    A class representing a listing

    Attributes:
        id (int): The unique identifier for the listing.
        name (str): The name for the listing
        num_bedrooms (int): The number of bedrooms for the listing
        num_bethrooms (int): The number of bethrooms for the listing
        garage (bool): Whether there is a garage or not in the listing
        price (float): The price for the listing
        zip_code (str): The zip code for the listing
        sold (bool): Whether the listing is sold or not
        date_created (date): The date the listing was created
        date_sold (date): The date the listing was sold

    Methods:
        __repr__(): Returns a string representation of the Listing object.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    num_bedrooms = db.Column(db.Integer)
    num_bethrooms = db.Column(db.Integer)
    garage = db.Column(db.Boolean)
    price = db.Column(db.Float)
    zip_code = db.Column(db.String(150))
    sold = db.Column(db.Boolean)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_sold = db.Column(db.DateTime)

    def __repr__(self):
        """
        Returns a string representation of the Listing object.

        Returns:
            str: A string representation of the Listing object, including the listing min and max price.
        """
        return f'<Listing "{self.name}">'
