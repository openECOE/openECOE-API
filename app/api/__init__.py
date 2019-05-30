from flask import Blueprint, current_app
from app import api_app as api
from flask_cors import CORS

bp = Blueprint('api', __name__)
CORS(bp, expose_headers='Content-Length, X-Total-Count')

# @bp.after_request
# def set_response_headers(response):
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     response.headers['Access-Control-Allow-Methods'] = 'GET, PUT, POST, PATCH, DELETE, OPTIONS'
#     response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
#     response.headers['Access-Control-Allow-Credentials'] = 'true'
#     response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
#     response.headers['Pragma'] = 'no-cache'
#     response.headers['Expires'] = '0'
#     response.headers['Access-Control-Expose-Headers'] = 'Content-Length, X-Total-Count'
#     return response


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
api.add_resource(StudentResource)
api.add_resource(PlannerResource)
api.add_resource(RoundResource)
api.add_resource(ShiftResource)
api.add_resource(StationResource)
api.add_resource(EcoeResource)
api.add_resource(OrganizationResource)