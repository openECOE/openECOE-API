import os
basedir = os.path.abspath(os.path.dirname(__file__))
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class BaseConfig:
    """Base configuration."""
    SERVER_NAME = os.environ.get('SERVER_NAME')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = os.environ.get('DEBUG')
    BCRYPT_LOG_ROUNDS = os.environ.get('BCRYPT_LOG_ROUNDS')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    API_AUTH = os.environ.get('API_AUTH')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    SERVER_NAME = "dev.api.openecoe.com:5000"
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    API_AUTH = False


class TestingConfig(BaseConfig):
    """Testing configuration."""
    SERVER_NAME = "test.api.openecoe.com:5000"
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'f24b05095b4748a8b9d13df5cdb8d83c'
    DEBUG = False
    API_AUTH = True
