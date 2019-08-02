from flask_potion import fields
from flask_potion.routes import Relation
from app.model.Schedule import Schedule
from app.api.ecoe import EcoePrincipalResource


class ScheduleResource(EcoePrincipalResource):
    events = Relation('events')

    class Meta:
        name = 'schedules'
        model = Schedule

    class Schema:
        ecoe = fields.ToOne('ecoes', nullable=True)
        stage = fields.ToOne('stages')
        station = fields.ToOne('stations', nullable=True)


