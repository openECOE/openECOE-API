from flask_potion import ModelResource, fields
from flask_potion.routes import Relation

from app.model.Day import Day
from app.model.Round import Round
from app.model.Shift import Shift

class DayResource(ModelResource):
    shifts = Relation('shift')

    class Meta:
        model = Day

    class Schema:
        ecoe = fields.ToOne('ecoe')
        date = fields.DateString()  # YYYY-MM-DD (eg 1997-07-16)


class ShiftResource(ModelResource):
    rounds = Relation('round')

    class Meta:
        model = Shift

    class Schema:
        day = fields.ToOne('day')
        start_time = fields.DateTimeString()  # YYYY-MM-DDThh:mm:ssTZD (eg 1997-07-16T19:20:30+01:00)


class RoundResource(ModelResource):
    students = Relation('student')

    class Meta:
        model = Round

    class Schema:
        shift = fields.ToOne('shift')
