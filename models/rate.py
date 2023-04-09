from sqlalchemy import Column, Integer, Float
from extensions import Base


class Rate(Base):
    """
    A class representing a rate

    Attributes:
        id (int): The unique identifier for the rate.
        min_price (int): The min price for the rate
        max_price (int): The max price for the rate
        rate (float): The rate for these prices

    Methods:
        __repr__(): Returns a string representation of the Rate object.
    """

    __tablename__ = "rate"
    id = Column(Integer, primary_key=True)
    min_price = Column(Integer)
    max_price = Column(Integer, nullable=True)
    rate = Column(Float)

    def __repr__(self):
        """
        Returns a string representation of the Rate object.

        Returns:
            str: A string representation of the Rate object, including the rate min and max price.
        """
        return f'<Rate "{self.min_price} to {self.max_price}">'
