from flask_potion import ModelResource, fields
from flask_potion.routes import Relation

from model.Shift import Shift

class ShiftResource(ModelResource):
    rounds = Relation('round')

    class Meta:
        model = Shift

    class Schema:
        day = fields.ToOne('day')
        start_time = fields.DateTimeString() #YYYY-MM-DDThh:mm:ssTZD (eg 1997-07-16T19:20:30+01:00)