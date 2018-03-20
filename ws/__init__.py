from flask_potion import Api
from start import app

from ws.organization import OrganizationResource
from ws.ecoe import EcoeResource
from ws.area import AreaResource
from ws.student import StudentResource
from ws.station import StationResource
from ws.group import GroupResource
from ws.question import QuestionResource
from ws.option import OptionResource

api = Api(app)

api.add_resource(OptionResource)
api.add_resource(QuestionResource)
api.add_resource(GroupResource)
api.add_resource(StationResource)
api.add_resource(StudentResource)
api.add_resource(AreaResource)
api.add_resource(EcoeResource)
api.add_resource(OrganizationResource)