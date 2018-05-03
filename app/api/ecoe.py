from flask_potion import ModelResource, fields
from flask_potion.routes import Relation
from app.model.ECOE import ECOE


class EcoeResource(ModelResource):
    areas = Relation('area')
    stations = Relation('station')
    schedules = Relation('schedule')
    students = Relation('student')
    wheels = Relation('wheel')
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
        wheels = fields.ToMany('wheel')
        shifts = fields.ToMany('shift')


