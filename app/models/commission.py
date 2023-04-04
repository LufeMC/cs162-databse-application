from app.extensions import db
import datetime


class Commission(db.Model):
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
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    total_commission = db.Column(db.Float)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        """
        Returns a string representation of the Commission object.

        Returns:
            str: A string representation of the Commission object, including the commission agent's id.
        """
        return f'<Commission of agent "{self.agent_id}">'
