from flask_potion import ModelResource, fields
from flask_potion.routes import Relation
from app.model.Schedule import Schedule


class ScheduleResource(ModelResource):
    events = Relation('event')

    class Meta:
        model = Schedule
        #natural_key = (
        #    ('ecoe', 'stage'),
        #    ('station', 'stage')
        #)

    class Schema:
        ecoe = fields.ToOne('ecoe', nullable=True)
        stage = fields.ToOne('stage')
        station = fields.ToOne('station', nullable=True)
        events = fields.ToMany('event')


