from flask_potion import ModelResource, fields
from flask_potion.routes import Relation
from app.model.Area import Area


class AreaResource(ModelResource):
    questions = Relation('question')

    class Meta:
        model = Area
        natural_key = 'name'

    class Schema:
        ecoe = fields.ToOne('ecoe')
        questions = fields.ToMany('question')


