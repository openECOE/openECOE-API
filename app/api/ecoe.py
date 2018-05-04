from flask_potion import ModelResource, fields
from flask_potion.routes import Relation
from app.model.ECOE import ECOE


class EcoeResource(ModelResource):
    areas = Relation('area')
    stations = Relation('station')
    schedules = Relation('schedule')
    students = Relation('student')
    rounds = Relation('round')
    shifts = Relation('shift')

    class Meta:
        model = ECOE
        natural_key = 'name'

    class Schema:
        organization = fields.ToOne('organization')
        areas = fields.ToMany('area')
        stations = fields.ToMany('station')
        schedules = fields.ToMany('schedule')
        students = fields.ToMany('student')
        rounds = fields.ToMany('round')
        shifts = fields.ToMany('shift')


