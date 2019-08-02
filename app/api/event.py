from flask_potion import fields
from app.model.Event import Event
from app.api.ecoe import EcoePrincipalResource


class EventResource(EcoePrincipalResource):
    class Meta:
        name = 'events'
        model = Event

    class Schema:
        schedule = fields.ToOne('schedules')

