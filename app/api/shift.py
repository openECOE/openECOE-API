from flask_potion import fields
from flask_potion.routes import Relation
from app.model.Shift import Shift
from app.api.ecoe import EcoePrincipalResource


class ShiftResource(EcoePrincipalResource):
    planners = Relation('planners')

    class Meta:
        name = 'shifts'
        model = Shift
        natural_key = ('ecoe', 'shift_code')

    class Schema:
        ecoe = fields.ToOne('ecoes')
        time_start = fields.DateTime()



