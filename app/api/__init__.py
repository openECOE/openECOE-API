from flask import Blueprint

bp = Blueprint('api', __name__)

from flask_potion import Api

from app.api.area import AreaResource
from app.api.day import DayResource
from app.api.ecoe import EcoeResource
from app.api.event import EventResource
from app.api.option import OptionResource
from app.api.organization import OrganizationResource
from app.api.qblock import QblockResource
from app.api.question import QuestionResource
from app.api.schedule import ScheduleResource
from app.api.shift import ShiftResource
from app.api.stage import StageResource
from app.api.station import StationResource
from app.api.student import StudentResource
from app.api.wheel import WheelResource
from app.api.user import UserResource

api = Api(bp)

api.add_resource(EventResource)
api.add_resource(ScheduleResource)
api.add_resource(StageResource)
api.add_resource(UserResource)
api.add_resource(OptionResource)
api.add_resource(QuestionResource)
api.add_resource(QblockResource)
api.add_resource(AreaResource)
api.add_resource(StudentResource)
api.add_resource(WheelResource)
api.add_resource(ShiftResource)
api.add_resource(StationResource)
api.add_resource(DayResource)
api.add_resource(EcoeResource)
api.add_resource(OrganizationResource)
