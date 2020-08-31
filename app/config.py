"""Flask configuration variables."""
from os import environ, path

basedir = path.abspath(path.dirname(__file__))

class Config:
    """Set Flask configuration from .env file."""
