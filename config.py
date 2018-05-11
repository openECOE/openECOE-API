import os
basedir = os.path.abspath(os.path.dirname(__file__))
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

local_base = os.environ.get('DATABASE_URL') or \
             'sqlite:///' + basedir
database_name = os.environ.get('DATABASE_NAME')


class BaseConfig:
    """Base configuration."""
    SERVER_NAME = "api.openecoe.com"
    SECRET_KEY = os.environ.get('SECRET_KEY', 'TEST_ECOE')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_AUTH = True
    SQLALCHEMY_DATABASE_URI = local_base + database_name


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
