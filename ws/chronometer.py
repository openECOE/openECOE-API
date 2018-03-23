from flask_potion import ModelResource, fields
from flask_potion.routes import Relation

from model.Chronometer import Chronometer

class ChronometerResource(ModelResource):
    alarms = Relation('ala')

    class Meta:
        model = Chronometer
