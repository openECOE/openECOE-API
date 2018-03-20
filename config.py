import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
   # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #                          'sqlite:///' + os.path.join(basedir, 'app.db')
   SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root@localhost/openECOE"
   #SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
   SQLALCHEMY_TRACK_MODIFICATIONS = False