from flask_potion import ModelResource, fields
from flask_potion.routes import Relation

from model.ECOE import ECOE

class EcoeResource(ModelResource):
    areas = Relation('area')
    days = Relation('day')

    class Meta:
        model = ECOE

    class Schema:
        organization = fields.ToOne('org')
        chronometers = fields.ToMany('chro')
        students = fields.ToMany('stu')