from flask_potion import ModelResource, fields
from flask_potion.routes import Relation
from app.model.Schedule import Schedule


class ScheduleResource(ModelResource):
    events = Relation('events')

    class Meta:
        name = 'schedules'
        model = Schedule

    class Schema:
        ecoe = fields.ToOne('ecoes', nullable=True)
        stage = fields.ToOne('stages')
        station = fields.ToOne('stations', nullable=True)


