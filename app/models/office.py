from app.extensions import db


class Office(db.Model):
    """
    A class representing a office

    Attributes:
        id (int): The unique identifier for the office.
        name (str): The user's name.
        agents (User): Office agents

    Methods:
        __repr__(): Returns a string representation of the Office object.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    agents = db.relationship('User', backref='post')

    def __repr__(self):
        """
        Returns a string representation of the Office object.

        Returns:
            str: A string representation of the Office object, including the office name.
        """
        return f'<Office "{self.name}">'
