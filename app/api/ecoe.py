from flask_potion import ModelResource, fields
from flask_potion.routes import Relation

from app.model.ECOE import ECOE


class EcoeResource(ModelResource):
    areas = Relation('area')
    days = Relation('day')

    class Meta:
        model = ECOE

    class Schema:
        organization = fields.ToOne('organization')
        chronometers = fields.ToMany('chronometer')
        students = fields.ToMany('student')
