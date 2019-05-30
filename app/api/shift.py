from flask_potion import ModelResource, fields
from flask_potion.routes import Relation
from app.model.Shift import Shift


class ShiftResource(ModelResource):
    planners = Relation('planner')

    class Meta:
        model = Shift
        natural_key = ('ecoe', 'shift_code')

    class Schema:
        ecoe = fields.ToOne('ecoe')
        time_start = fields.DateTime()



