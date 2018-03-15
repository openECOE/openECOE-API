from ws import app
from model.Organization import Organization
from model.ECOE import ECOE
from flask_potion import Api, ModelResource, fields
from flask_potion.routes import Relation

# #These imports are necesary, if you don't do the imports, it won't recognize the URIs
# from ws import organization
# from ws import user
# from ws import permission
# from ws import ecoe
# from ws import area
# from ws import alarm
# from ws import station
# from ws import group
# from ws import question
# from ws import option
# from ws import chronometer
# from ws import student
# from ws import day
# from ws import shift
# from ws import round

api = Api(app)

class EcoeResource(ModelResource):
    class Meta:
        model = ECOE

    class Schema:
        organization = fields.ToOne('org')

api.add_resource(EcoeResource)

class OrganizationResource(ModelResource):
    ecoes = Relation('ecoe')

    class Meta:
        model = Organization

api.add_resource(OrganizationResource)

app.run(port=5000, debug=True)

