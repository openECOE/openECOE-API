#  Copyright (c) 2019 Miguel Hernandez University of Elche
#  This file is part of openECOE-API.
#
#      openECOE-API is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      openECOE-API is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with openECOE-API.  If not, see <https://www.gnu.org/licenses/>.

from flask import Blueprint
from app import openecoe_api as api
from flask_cors import CORS
import flask_excel as excel

from app.api.area import AreaResource
from app.api.ecoe import EcoeResource
from app.api.event import EventResource
from app.api.organization import OrganizationResource
from app.api.question import QuestionResource, BlockResource
from app.api.schedule import ScheduleResource
from app.api.shift import ShiftResource
from app.api.stage import StageResource
from app.api.station import StationResource
from app.api.student import AnswerResource, StudentResource
from app.api.planner import PlannerResource
from app.api.round import RoundResource
from app.api.user import UserResource, RoleResource, PermissionResource


bp = Blueprint('api', __name__)
CORS(bp, expose_headers='Content-Length, X-Total-Count')
excel.init_excel(bp)

version = 'v1'

api.prefix = '/' + version
api.title = 'openECOE API ' + version

api.add_resource(EventResource)
api.add_resource(ScheduleResource)
api.add_resource(StageResource)
api.add_resource(RoleResource)
api.add_resource(PermissionResource)
api.add_resource(AnswerResource)
api.add_resource(QuestionResource)
api.add_resource(BlockResource)
api.add_resource(AreaResource)
api.add_resource(StudentResource)
api.add_resource(PlannerResource)
api.add_resource(RoundResource)
api.add_resource(ShiftResource)
api.add_resource(StationResource)
api.add_resource(EcoeResource)
api.add_resource(UserResource)
api.add_resource(OrganizationResource)

api.init_app(bp)
