from flask_potion import ModelResource, fields
from app.model.Stage import Stage


class StageResource(ModelResource):
    class Meta:
        model = Stage

    class Schema:
        schedules = fields.ToMany('schedule')

