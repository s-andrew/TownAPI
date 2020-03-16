from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restplus import Api
from flask_sqlalchemy_session import flask_scoped_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.views.auth import api as auth_namespace
from app.views.districts import api as district_namespace
from app.views.towns import api as towns_namespace


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    engine = create_engine(app.config['SQLALCHEMY_DB_URI'], echo=app.config['SQLALCHEMY_ECHO'])
    flask_scoped_session(sessionmaker(bind=engine), app)

    JWTManager(app)

    api = Api(
        app,
        description='OLOLO',
        authorizations={
            'JWT Access': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization'
            },
            'JWT Refresh': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization'
            },
        },
    )
    api.add_namespace(auth_namespace)
    api.add_namespace(towns_namespace)
    api.add_namespace(district_namespace)

    return app
