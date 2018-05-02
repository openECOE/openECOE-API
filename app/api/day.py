from flask_potion import ModelResource, fields

from app.model.Day import Day
from app.model.Wheel import Wheel
from app.model.Shift import Shift


class DayResource(ModelResource):
    class Meta:
        model = Day

    class Schema:
        ecoes = fields.ToMany('ecoe')
        shifts = fields.ToMany('shift')
        date = fields.DateString()  # YYYY-MM-DD (eg 1997-07-16)


class ShiftResource(ModelResource):
    class Meta:
        model = Shift
        natural_key = ('code', 'id_day')

    class Schema:
        day = fields.ToOne('day')
        wheels = fields.ToMany('wheel')


class WheelResource(ModelResource):
    class Meta:
        model = Wheel
        natural_key = ('code', 'id_shift')

    class Schema:
        shift = fields.ToOne('shift')
        students = fields.ToMany('student')
