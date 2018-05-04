from flask_potion import ModelResource, fields
from flask_potion.routes import Relation
from app.model.Round import Round


class RoundResource(ModelResource):
    planners = Relation('planner')

    class Meta:
        model = Round
        natural_key = ('ecoe', 'round_code')

    class Schema:
        ecoe = fields.ToOne('ecoe')
        planners = fields.ToMany('planner')
