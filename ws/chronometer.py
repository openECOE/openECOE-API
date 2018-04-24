from flask_potion import ModelResource, fields
from flask_potion.routes import Relation
from model.Chronometer import Chronometer
from model.Alarm import Alarm


class ChronometerResource(ModelResource):
    ecoes = Relation('ecoe')
    alarms = Relation('alarm')
    stations = Relation('station')

    class Meta:
        model = Chronometer
        natural_key = ('name')


class AlarmResource(ModelResource):

    class Meta:
        model = Alarm

    class Schema:
        chronometer = fields.ToOne('chronometer')
