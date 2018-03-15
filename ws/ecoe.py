from flask_potion import ModelResource, fields

from model import ECOE

class EcoeResource(ModelResource):
    class Meta:
        model = ECOE

    class Schema:
        organization = fields.ToOne('org')