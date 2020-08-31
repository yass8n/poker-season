"""Flask configuration variables."""
from os import environ, path

basedir = path.abspath(path.dirname(__file__))

class Config:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = environ.get('POKER_SECRET_KEY')
    FLASK_APP = environ.get('POKER_FLASK_APP')
    FLASK_ENV = environ.get('POKER_FLASK_ENV')

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False