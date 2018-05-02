from flask_potion import ModelResource, fields
from app.model.Day import Day


class DayResource(ModelResource):
    class Meta:
        model = Day

    class Schema:
        ecoes = fields.ToMany('ecoe')
        shifts = fields.ToMany('shift')
        date = fields.DateString()  # YYYY-MM-DD (eg 1997-07-16)
