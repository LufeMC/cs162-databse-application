from app.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.Text)
    firstName = db.Column(db.String(150))
    lastName = db.Column(db.String(150))
    email = db.Column(db.String(150))
    password = db.Column(db.Text)
    tasks = db.relationship('Task', backref='post')

    def __repr__(self):
        return f'<User "{self.firstName} {self.lastName}">'
