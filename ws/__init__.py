from model import *

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_potion import Api, ModelResource, fields
from flask_potion.routes import Relation, FieldSet, Schema, ItemRoute, Route

from flask import jsonify, request

import json
import datetime

from werkzeug.exceptions import abort, Response

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/angelsegura/PycharmProjects/openECOE-API/ecoe.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/openECOE'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)



