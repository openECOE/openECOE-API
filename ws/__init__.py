from flask_potion import Api
from start import app
from model.Organization import Organization
from model.ECOE import ECOE

from ws.ecoe import EcoeResource
from ws.organization import OrganizationResource

api = Api(app)

api.add_resource(EcoeResource)
api.add_resource(OrganizationResource)