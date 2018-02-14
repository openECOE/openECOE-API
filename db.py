from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/angelsegura/PycharmProjects/openECOE-API/ecoe.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/ecoe'

db = SQLAlchemy(app)

