import os
basedir = os.path.abspath(os.path.dirname(__file__))
from app.main import app

class Config(object):
    DEBUG = True
    TESTING = True
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ['POKER_DATABASE_URL']
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['FLASK_DEBUG'] = True


class ProductionConfig(Config):
    DEBUG = True


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True