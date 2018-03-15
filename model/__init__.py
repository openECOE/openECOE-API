from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# from .Alarm import Alarm
# from .Area import Area
# from .Chronometer import Chronometer
# from .Day import Day
from .ECOE import ECOE
# from .Group import Group
# from .Option import Option
from .Organization import Organization
# from .Permission import Permission
# from .Question import Question
# from .Round import Round
# from .Shift import Shift
# from .Station import Station
# from .User import User
