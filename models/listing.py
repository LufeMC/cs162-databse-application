from sqlalchemy import Column, Integer, Boolean, Float, DateTime, String
from extensions import Base
import datetime


class Listing(Base):
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

    __tablename__ = "listing"
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    num_bedrooms = Column(Integer)
    num_bethrooms = Column(Integer)
    garage = Column(Boolean)
    price = Column(Float)
    zip_code = Column(String(150))
    sold = Column(Boolean)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    date_sold = Column(DateTime)

    def __repr__(self):
        """
        Returns a string representation of the Listing object.

        Returns:
            str: A string representation of the Listing object, including the listing min and max price.
        """
        return f'<Listing "{self.name}">'
