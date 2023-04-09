from sqlalchemy import Column, Integer, String, Text, ForeignKey
from extensions import Base


class User(Base):
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

    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    email = Column(String(150))
    password = Column(Text)
    type = Column(String(150), default="buyer")
    office_id = Column(Integer, ForeignKey("office.id"))

    def __repr__(self):
        """
        Returns a string representation of the User object.

        Returns:
            str: A string representation of the User object, including the user name.
        """
        return f'<User "{self.name}">'
