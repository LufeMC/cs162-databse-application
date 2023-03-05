from app.extensions import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Text)
    name = db.Column(db.String(150))
    description = db.Column(db.String(150))
    deleted = db.Column(db.Boolean)
    status = db.Column(db.String(15))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Task "{self.name}">'
