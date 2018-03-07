import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('mysql+pymysql://root@localhost/openECOE')
    SQLALCHEMY_TRACK_MODIFICATIONS = False