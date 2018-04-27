from flask import Blueprint

bp = Blueprint('api', __name__)

from flask_potion import Api
from app.auth.auth import token_auth
from flask_login import login_required

from app.api.organization import OrganizationResource
from app.api.ecoe import EcoeResource
from app.api.area import AreaResource
from app.api.student import StudentResource
from app.api.station import StationResource
from app.api.group import GroupResource
from app.api.question import QuestionResource, OptionResource, AnswerResource
from app.api.day import DayResource, ShiftResource, RoundResource
from app.api.chronometer import ChronometerResource, AlarmResource

api = Api(bp)

api.add_resource(AnswerResource)
api.add_resource(StudentResource)
api.add_resource(RoundResource)
api.add_resource(ShiftResource)
api.add_resource(DayResource)
api.add_resource(OptionResource)
api.add_resource(QuestionResource)
api.add_resource(GroupResource)
api.add_resource(StationResource)
api.add_resource(AreaResource)
api.add_resource(EcoeResource)
api.add_resource(AlarmResource)
api.add_resource(ChronometerResource)
api.add_resource(OrganizationResource)

from app.api import user
