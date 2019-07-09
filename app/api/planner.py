from flask_potion import ModelResource, fields
from flask_potion.routes import Relation
from app.model.Planner import Planner


class PlannerResource(ModelResource):
    students = Relation('students')

    class Meta:
        name = 'planners'
        model = Planner

    class Schema:
        shift = fields.ToOne('shifts')
        round = fields.ToOne('rounds')
