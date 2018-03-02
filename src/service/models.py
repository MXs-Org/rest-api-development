import json

from database import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    fullname = db.Column(db.String(128))
    age = db.Column(db.Integer)
    entries = db.relationship('Entry', backref='author', lazy='dynamic')
    token = db.relationship('Token', backref='user', uselist=False)

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def json_dict(self):
        # Returns a Python dictionary of public attributes
        dct = {
            'username': self.username,
            'fullname': self.fullname,
            'age': self.age
        }
        return dct

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(36), index=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # author = db.Column(db.String(64), index=True) # username of author, maybe use foreign key user_id
    publish_date = db.Column(db.String(26))
    public = db.Column(db.Boolean)
    text = db.Column(db.Text)

    def __repr__(self):
        return "<Diary Entry {}>".format(self.title)

    def json_dict(self):
        # Returns a Python dictionary of public attributes
        username = User.query.filter_by(id=self.user_id).first().username
        dct = {
            'id': self.id,
            'title': self.title,
            'author': username,
            'publish_date': self.publish_date,
            'public': self.public,
            'text': self.text
        }
        return dct
