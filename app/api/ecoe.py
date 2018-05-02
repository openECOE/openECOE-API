from flask_potion import ModelResource, fields
from app.model.ECOE import ECOE


class EcoeResource(ModelResource):
    class Meta:
        model = ECOE
        natural_key = 'name'

    class Schema:
        organization = fields.ToOne('organization')

        areas = fields.ToMany('area')
        stations = fields.ToMany('station')
        schedules = fields.ToMany('schedule')
        students = fields.ToMany('student')
        days = fields.ToMany('day')
