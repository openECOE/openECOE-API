from flask import Blueprint

bp = Blueprint('api', __name__)

from flask_potion import Api
from flask_login import login_required

api = Api(bp, decorators=[login_required])

from app.api.ecoe import EcoeResource
from app.api.area import AreaResource
from app.api.student import StudentResource
from app.api.station import StationResource
from app.api.group import GroupResource
from app.api.question import QuestionResource
from app.api.option import OptionResource
from app.api.day import DayResource
from app.api.shift import ShiftResource
from app.api.chronometer import ChronometerResource
from app.api.alarm import AlarmResource
from app.api.round import RoundResource

api.add_resource(RoundResource)
api.add_resource(ShiftResource)
api.add_resource(DayResource)
api.add_resource(OptionResource)
api.add_resource(QuestionResource)
api.add_resource(GroupResource)
api.add_resource(StationResource)
api.add_resource(AreaResource)
api.add_resource(EcoeResource)
api.add_resource(StudentResource)
api.add_resource(AlarmResource)
api.add_resource(ChronometerResource)

from app.api import user, organization
from app.api import tokens
