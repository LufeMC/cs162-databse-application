from app.extensions import db


class User(db.Model):
    """
    A class representing a user in the kanban app.

    Attributes:
        id (int): The unique identifier for the task.
        uuid (str): A Universally Unique Identifier (UUID) for the task.
        firstName (str): The user's first name.
        lastName (str): The user's last name.
        email (str): The user's email.
        password (str): The user's password.
        user_id (Tasks): List of tasks associated with that user.

    Methods:
        __repr__(): Returns a string representation of the Task object.
    """
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Text)
    firstName = db.Column(db.String(150))
    lastName = db.Column(db.String(150))
    email = db.Column(db.String(150))
    password = db.Column(db.Text)
    tasks = db.relationship('Task', backref='post')

    def __repr__(self):
        """
        Returns a string representation of the User object.

        Returns:
            str: A string representation of the User object, including the user first and last name.
        """
        return f'<User "{self.firstName} {self.lastName}">'
