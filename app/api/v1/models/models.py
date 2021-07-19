from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from sqlalchemy import inspect
from app.extensions import db


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(250))

    def __init__(self, username=None, email=None, password=None):
        super().__init__()
        self.username = username
        self.email = email
        if password:
            self.password = generate_password_hash(password)

    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return "<User '{}'>".format(self.username)


class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=False)
    room = db.Column(db.String(500), unique=False)
    message = db.Column(db.String(500), unique=False)

    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return "<ChatHistory '{}', '{}', '{}'>".format(self.username, self.room, self.message)
