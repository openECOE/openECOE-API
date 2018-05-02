from flask_potion import ModelResource, fields
from flask_potion.routes import Relation
from app.model.Shift import Shift


class ShiftResource(ModelResource):
    wheels = Relation('wheel')

    class Meta:
        model = Shift
        natural_key = ('code', 'day')

    class Schema:
        day = fields.ToOne('day')


