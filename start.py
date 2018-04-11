from flask import Flask
from config import Config
# from model import db
# from model.User import User

app = Flask(__name__)
app.config.from_object(Config)

from ws import *

# db.session.add(User(name='admin', surname='admin', is_superadmin=True))
# db.session.commit()
