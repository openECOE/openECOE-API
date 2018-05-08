import os
basedir = os.path.abspath(os.path.dirname(__file__))
local_base = os.environ.get('DATABASE_URL') or \
             'sqlite:///' + basedir
database_name = os.environ.get('DATABASE_NAME')


class BaseConfig:
    """Base configuration."""
    SERVER_NAME = "api.openecoe.com:5000"
    SECRET_KEY = os.getenv('SECRET_KEY', 'TEST_ECOE')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_AUTH = True


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = local_base + database_name


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = local_base + database_name + '_test'
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'my_precious'
    DEBUG = False
    API_AUTH = True
    SQLALCHEMY_DATABASE_URI = local_base + database_name + '_prod'
