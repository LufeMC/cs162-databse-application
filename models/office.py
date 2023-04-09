from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from extensions import Base


class Office(Base):
    """
    A class representing a office

    Attributes:
        id (int): The unique identifier for the office.
        name (str): The user's name.
        agents (User): Office agents

    Methods:
        __repr__(): Returns a string representation of the Office object.
    """

    __tablename__ = "office"
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    agents = relationship("User", backref="post")

    def __repr__(self):
        """
        Returns a string representation of the Office object.

        Returns:
            str: A string representation of the Office object, including the office name.
        """
        return f'<Office "{self.name}">'
