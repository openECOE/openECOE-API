from flask import Blueprint
from app import api_app as api

bp = Blueprint('api', __name__)

@bp.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


api.init_app(bp)

from app.api.area import AreaResource
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
from app.api.planner import PlannerResource
from app.api.round import RoundResource
from app.api.user import UserResource

api.add_resource(EventResource)
api.add_resource(ScheduleResource)
api.add_resource(StageResource)
api.add_resource(UserResource)
api.add_resource(OptionResource)
api.add_resource(QuestionResource)
api.add_resource(QblockResource)
api.add_resource(AreaResource)
api.add_resource(PlannerResource)
api.add_resource(StudentResource)
api.add_resource(RoundResource)
api.add_resource(ShiftResource)
api.add_resource(StationResource)
api.add_resource(EcoeResource)
api.add_resource(OrganizationResource)
