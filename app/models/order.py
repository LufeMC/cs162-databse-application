from app.extensions import db
import datetime


class Order(db.Model):
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
    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'))
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    agent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        """
        Returns a string representation of the Order object.

        Returns:
            str: A string representation of the Order object, including the order id.
        """
        return f'<Order "{self.id}">'
