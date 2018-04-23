from flask_potion import ModelResource, fields

from app.model.Alarm import Alarm

class AlarmResource(ModelResource):

    class Meta:
        model = Alarm

    class Schema:
        chronometer = fields.ToOne('chronometer')