from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from extensions import Base


class Commission(Base):
    """
    A class representing a commission.

    Attributes:
        id (int): The unique identifier for the commission.
        agent_id (User): Listing agent
        total_comission (float): Total commission the agent should get at this month
        date_created (date): The date the commission was created

    Methods:
        __repr__(): Returns a string representation of the Commission object.
    """

    __tablename__ = "commission"
    id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey("user.id"))
    total_commission = Column(Float)
    month = Column(DateTime)

    def __repr__(self):
        """
        Returns a string representation of the Commission object.

        Returns:
            str: A string representation of the Commission object, including
            the commission agent's id.
        """
        return f'<Commission of agent "{self.agent_id}">'
