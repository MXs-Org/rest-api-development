from database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    fullname = db.Column(db.String(128))
    age = db.Column(db.Integer)

    def __repr__(self):
        return "<User {}>".format(self.username)
    