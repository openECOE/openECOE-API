from flask_potion import ModelResource, fields
from flask_potion.routes import Relation

from model.Station import Station

class StationResource(ModelResource):
    groups = Relation('group')

    class Meta:
        model = Station

    class Schema:
        ecoe = fields.ToOne('ecoe')
        chronometers = fields.ToMany('chro')