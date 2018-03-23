from flask_potion import ModelResource, fields
from flask_potion.routes import Relation

from model.Day import Day

class DayResource(ModelResource):
   # shifts = Relation('shi')

    class Meta:
        model = Day

    class Schema:
        ecoe = fields.ToOne('ecoe')
        date = fields.DateString() # YYYY-MM-DD (eg 1997-07-16)