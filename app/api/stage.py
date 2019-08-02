from flask_potion.routes import Relation
from app.model.Stage import Stage
from app.api.ecoe import EcoePrincipalResource


class StageResource(EcoePrincipalResource):
    schedules = Relation('schedules')

    class Meta:
        name = 'stages'
        model = Stage


