from flask_potion import ModelResource, fields
from flask_potion.routes import Relation

from model.Day import Day

class DayResource(ModelResource):
    #questions = Relation('ques')

    class Meta:
        model = Day

    class Schema:
        ecoe = fields.ToOne('ecoe')
        date = fields.DateTimeString() # YYYY-MM-DDThh:mm:ssTZD (eg 1997-07-16T19:20:30+01:00)