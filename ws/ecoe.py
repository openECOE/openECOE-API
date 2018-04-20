from flask_potion import ModelResource, fields
from flask_potion.routes import Relation
from model.ECOE import ECOE


class EcoeResource(ModelResource):
    areas = Relation('area')
    days = Relation('day')
    students = Relation('student')

    class Meta:
        model = ECOE

    class Schema:
        organization = fields.ToOne('organization')
        chronometers = fields.ToMany('chronometer')
