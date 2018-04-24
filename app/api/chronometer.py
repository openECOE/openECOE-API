from flask_potion import ModelResource
from flask_potion.routes import Relation

from app.model.Chronometer import Chronometer

class ChronometerResource(ModelResource):
    ecoes = Relation('ecoe')
    alarms = Relation('alarm')
    stations = Relation('station')

    class Meta:
        model = Chronometer
