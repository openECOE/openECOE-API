from flask_potion import ModelResource, fields
from app.model.Planner import Planner


class PlannerResource(ModelResource):

    class Meta:
        model = Planner

    class Schema:
        shift = fields.ToOne('shift')
        round = fields.ToOne('round')
        students = fields.ToMany('student')
