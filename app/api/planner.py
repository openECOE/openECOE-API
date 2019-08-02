from flask_potion import fields
from flask_potion.routes import Relation
from app.model.Planner import Planner
from app.api.ecoe import EcoePrincipalResource


class PlannerResource(EcoePrincipalResource):
    students = Relation('students')

    class Meta:
        name = 'planners'
        model = Planner

    class Schema:
        shift = fields.ToOne('shifts')
        round = fields.ToOne('rounds')
