from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask import jsonify, request
import json
from werkzeug.exceptions import abort, Response

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/angelsegura/PycharmProjects/openECOE-API/ecoe.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/ecoe'

db = SQLAlchemy(app)

