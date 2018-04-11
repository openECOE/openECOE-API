from flask_login import login_required
from flask_potion import Api
from start import app
import login

api = Api(app, decorators=[login_required])

from ws.organization import OrganizationResource
from ws.ecoe import EcoeResource
from ws.area import AreaResource
from ws.student import StudentResource
from ws.station import StationResource
from ws.group import GroupResource
from ws.question import QuestionResource
from ws.option import OptionResource
from ws.day import DayResource
from ws.shift import ShiftResource
from ws.chronometer import ChronometerResource
from ws.alarm import AlarmResource
from ws.round import RoundResource
from ws import user


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
api.add_resource(OrganizationResource)