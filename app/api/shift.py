from flask_potion import ModelResource, fields
from flask_potion.routes import Relation
from app.model.Shift import Shift


class ShiftResource(ModelResource):
    planners = Relation('planners')

    class Meta:
        name = 'shifts'
        model = Shift
        natural_key = ('ecoe', 'shift_code')

    class Schema:
        ecoe = fields.ToOne('ecoes')
        time_start = fields.DateTime()



