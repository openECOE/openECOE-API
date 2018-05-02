from flask_potion import ModelResource, fields
from app.model.Schedule import Schedule


class ScheduleResource(ModelResource):
    class Meta:
        model = Schedule
        natural_key = (
            ('id_ecoe', 'id_stage'),
            ('id_station', 'id_stage')
        )

    class Schema:
        ecoe = fields.ToOne('ecoe')
        stage = fields.ToOne('stage')
        station = fields.ToOne('station')
        events = fields.ToMany('event')

