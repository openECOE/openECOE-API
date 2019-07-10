from flask import Blueprint
from app import api_app as api
from flask_cors import CORS

from .area import AreaResource
from .ecoe import EcoeResource
from .event import EventResource
from .option import OptionResource
from .organization import OrganizationResource
from .qblock import QblockResource
from .question import QuestionResource
from .schedule import ScheduleResource
from .shift import ShiftResource
from .stage import StageResource
from .station import StationResource
from .student import StudentResource
from .planner import PlannerResource
from .round import RoundResource
from .user import UserResource, RoleResource, PermissionResource


bp = Blueprint('api', __name__)
CORS(bp, expose_headers='Content-Length, X-Total-Count')

version = 'v1'

api.prefix = '/' + version
api.title = 'openECOE API ' + version

api.add_resource(EventResource)
api.add_resource(ScheduleResource)
api.add_resource(StageResource)
api.add_resource(RoleResource)
api.add_resource(PermissionResource)
api.add_resource(UserResource)
api.add_resource(OptionResource)
api.add_resource(QuestionResource)
api.add_resource(QblockResource)
api.add_resource(AreaResource)
api.add_resource(StudentResource)
api.add_resource(PlannerResource)
api.add_resource(RoundResource)
api.add_resource(ShiftResource)
api.add_resource(StationResource)
api.add_resource(EcoeResource)
api.add_resource(OrganizationResource)

api.init_app(bp)
