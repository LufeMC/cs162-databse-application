from app.extensions import db


class User(db.Model):
    """
    A class representing a user.

    Attributes:
        id (int): The unique identifier for the user.
        name (str): The user's name.
        lastName (str): The user's last name.
        password (str): The user's password.
        type (str): A user type (default: buyer)
        office_id (Office): Office id from the user

    Methods:
        __repr__(): Returns a string representation of the User object.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150))
    password = db.Column(db.Text)
    type = db.Column(db.String(150), default="buyer")
    office_id = db.Column(db.Integer, db.ForeignKey('office.id'))

    def __repr__(self):
        """
        Returns a string representation of the User object.

        Returns:
            str: A string representation of the User object, including the user name.
        """
        return f'<User "{self.name}">'
