import os
from ast import literal_eval
basedir = os.path.abspath(os.path.dirname(__file__))
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    BCRYPT_LOG_ROUNDS = literal_eval(os.environ.get('BCRYPT_LOG_ROUNDS'))
    DEBUG = literal_eval(os.environ.get('DEBUG'))
    TESTING = literal_eval(os.environ.get('TESTING'))
    SQLALCHEMY_TRACK_MODIFICATIONS = literal_eval(os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS'))
    API_AUTH = literal_eval(os.environ.get('API_AUTH'))
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
