import sys
import os

from flask import Flask
from flask_script import Manager

from models import db
from models.user import User
from models.article import Article

app = Flask(__name__)
db_path = 'chat.sqlite'
manager = Manager(app)


def register_routes(app):
    from huangdmin import HuangAdmin
    ca = HuangAdmin(app, db, [User, Article, ])
    ca.init_app()


def configure_app():
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.secret_key = 'web chat key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)
    db.init_app(app)
    register_routes(app)


def configured_app():
    configure_app()
    return app


def nth_folder(n, file):
    path = os.path.abspath(file)
    while n > 0:
        path = os.path.dirname(path)
        n -= 1
    return path


def insert_path():
    path = nth_folder(3, __file__)
    sys.path.insert(0, path)


def server():
    insert_path()
    configure_app()
    config = dict(
        debug=True,
        host='127.0.0.1',
        port=5000,
        threaded=True,
    )
    app.run(**config)

if __name__ == '__main__':
    server()
