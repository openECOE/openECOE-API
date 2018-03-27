from flask_potion import ModelResource, fields
from flask_potion.routes import Relation

from model.Chronometer import Chronometer

class ChronometerResource(ModelResource):
    ecoes = Relation('ecoe')
    alarms = Relation('ala')
    stations = Relation('sta')

    class Meta:
        model = Chronometer
