from flask_potion import ModelResource, fields
from app.model.Shift import Shift


class ShiftResource(ModelResource):
    class Meta:
        model = Shift
        natural_key = ('code', 'id_day')

    class Schema:
        day = fields.ToOne('day')
        wheels = fields.ToMany('wheel')

