from sqlalchemy import Column, Integer, ForeignKey, DateTime
from extensions import Base
import datetime


class Order(Base):
    """
    A class representing a order.

    Attributes:
        id (int): The unique identifier for the order.
        listing_id (Listing): Id of the Listing related to the order
        buyer_id (User): Listing buyer
        agent_id (User): Listing agent
        date_created (date): The date the order was created

    Methods:
        __repr__(): Returns a string representation of the Order object.
    """

    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey("listing.id"))
    buyer_id = Column(Integer, ForeignKey("user.id"))
    agent_id = Column(Integer, ForeignKey("user.id"))
    date_created = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        """
        Returns a string representation of the Order object.

        Returns:
            str: A string representation of the Order object, including the order id.
        """
        return f'<Order "{self.id}">'
