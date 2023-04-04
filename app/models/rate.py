from app.extensions import db


class Rate(db.Model):
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
    id = db.Column(db.Integer, primary_key=True)
    min_price = db.Column(db.Integer)
    max_price = db.Column(db.Integer)
    rate = db.Column(db.Float)

    def __repr__(self):
        """
        Returns a string representation of the Rate object.

        Returns:
            str: A string representation of the Rate object, including the rate min and max price.
        """
        return f'<Rate "{self.min_price} to {self.max_price}">'
