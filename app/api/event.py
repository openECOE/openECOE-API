from flask_potion import ModelResource, fields
from app.model.Event import Event


class EventResource(ModelResource):
    class Meta:
        name = 'events'
        model = Event

    class Schema:
        schedule = fields.ToOne('schedules')

