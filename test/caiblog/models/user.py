#!encoding=utf-8

from . import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode())
    password = db.Column(db.String())
    email = db.Column(db.String(), nullable=True)

    article = db.relationship('Article', backref='user')
