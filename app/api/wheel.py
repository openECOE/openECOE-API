from flask_potion import ModelResource, fields
from flask_potion.routes import Relation
from app.model.Wheel import Wheel


class WheelResource(ModelResource):
    planners = Relation('planner')

    class Meta:
        model = Wheel
        natural_key = ('ecoe', 'wheel_code')

    class Schema:
        ecoe = fields.ToOne('ecoe')
        planners = fields.ToMany('planner')
