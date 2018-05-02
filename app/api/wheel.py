from flask_potion import ModelResource, fields
from app.model.Wheel import Wheel


class WheelResource(ModelResource):
    class Meta:
        model = Wheel
        natural_key = ('code', 'id_shift')

    class Schema:
        shift = fields.ToOne('shift')
        students = fields.ToMany('student')


