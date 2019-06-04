from flask_potion import ModelResource, fields
from flask_potion.routes import Relation
from app.model.Planner import Planner


class PlannerResource(ModelResource):
    students = Relation('student')

    class Meta:
        model = Planner

    class Schema:
        shift = fields.ToOne('shift')
        round = fields.ToOne('round')
