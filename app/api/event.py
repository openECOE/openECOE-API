from flask_potion import ModelResource, fields
from app.model.Event import Event


class EventResource(ModelResource):
    class Meta:
        model = Event

    class Schema:
        schedule = fields.ToOne('schedule')

