from flask_potion import ModelResource, fields
from flask_potion.routes import Relation
from app.model.Wheel import Wheel


class WheelResource(ModelResource):
    students = Relation('student')

    class Meta:
        model = Wheel
        natural_key = ('code', 'shift')

    class Schema:
        shift = fields.ToOne('shift')



