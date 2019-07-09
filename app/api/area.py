from flask_potion import ModelResource, fields
from flask_potion.routes import Relation
from app.model.Area import Area


class AreaResource(ModelResource):
    questions = Relation('questions')

    class Meta:
        name = 'areas'
        model = Area
        natural_key = 'name'

    class Schema:
        ecoe = fields.ToOne('ecoes')


