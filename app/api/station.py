from flask_potion import ModelResource, fields
from app.model.Station import Station


class StationResource(ModelResource):
    class Meta:
        model = Station
        natural_key = 'name'

    class Schema:
        ecoe = fields.ToOne('ecoe')
        schedules = fields.ToMany('schedule')
        qblocks = fields.ToMany('qblock')

