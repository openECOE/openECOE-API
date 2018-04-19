from flask_potion import Api
from start import app
from auth import login_required

api = Api(app, decorators=[login_required])

from api.ecoe import EcoeResource
from api.area import AreaResource
from api.student import StudentResource
from api.station import StationResource
from api.group import GroupResource
from api.question import QuestionResource
from api.option import OptionResource
from api.day import DayResource
from api.shift import ShiftResource
from api.chronometer import ChronometerResource
from api.alarm import AlarmResource
from api.round import RoundResource

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

from api import user, organization
from api import tokens
