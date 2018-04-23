from flask_potion import ModelResource, fields
from flask_potion.routes import Relation

from app.model.Day import Day

class DayResource(ModelResource):
    shifts = Relation('shift')

    class Meta:
        model = Day

    class Schema:
        ecoe = fields.ToOne('ecoe')
        date = fields.DateString() # YYYY-MM-DD (eg 1997-07-16)