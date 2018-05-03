from flask_potion import ModelResource, fields
from flask_potion.routes import Relation
from app.model.Day import Day


#TODO: Review relation with ECOE (ToMany or ToOne?)
class DayResource(ModelResource):
    # ecoes = Relation('ecoe')
    shifts = Relation('shift')

    class Meta:
        model = Day
        natural_key = 'date'

    class Schema:
        date = fields.DateString()  # YYYY-MM-DD (eg 1997-07-16)
        shifts = fields.ToMany('shift')

