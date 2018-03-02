from model import *
from ws import *

from ws import organization
from ws import user
from ws import permission
from ws import ecoe
from ws import area
from ws import alarm
from ws import station
from ws import group
from ws import question
from ws import option
from ws import chronometer
from ws import student
from ws import day
from ws import shift
from ws import round

class OrganizationResource(ModelResource):
    class Meta:
        model = Organization

api = Api(app)
api.add_resource(OrganizationResource)

app.run(port=5000, debug=True)