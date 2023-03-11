from app.extensions import db


class Task(db.Model):
    """
    A class representing a task in the kanban app.

    Attributes:
        id (int): The unique identifier for the task.
        uuid (str): A Universally Unique Identifier (UUID) for the task.
        name (str): The name of the task.
        description (str): A description of the task.
        deleted (bool): A flag indicating whether the task has been deleted.
        status (int): The status of the task (toDo, doing or done), represented as an integer.
        user_id (int): The ID of the user who created the task.

    Methods:
        __repr__(): Returns a string representation of the Task object.
    """
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Text)
    name = db.Column(db.String(150))
    description = db.Column(db.String(150))
    deleted = db.Column(db.Boolean, default=False)
    status = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        """
        Returns a string representation of the Task object.

        Returns:
            str: A string representation of the Task object, including the task name.
        """
        return f'<Task "{self.name}">'
