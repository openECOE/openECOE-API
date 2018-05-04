from flask_potion import ModelResource, fields
from flask_potion.routes import Relation
from app.model.Station import Station


class StationResource(ModelResource):
    schedules = Relation('schedule')
    qblocks = Relation('qblock')

    class Meta:
        model = Station
        natural_key = 'name'

    class Schema:
        ecoe = fields.ToOne('ecoe')


