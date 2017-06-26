#!encoding=utf-8

from . import db


class Article(db.Model):
    __tablename__ = 'channels'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(20))
    tag = db.Column(db.Unicode(100))
    created_time = db.Column(db.Integer)
    update_time = db.Column(db.Integer)
    content = db.Column(db.Unicode(10000))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
