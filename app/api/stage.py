from flask_potion import ModelResource
from flask_potion.routes import Relation
from app.model.Stage import Stage


class StageResource(ModelResource):
    schedules = Relation('schedules')

    class Meta:
        name = 'stages'
        model = Stage


