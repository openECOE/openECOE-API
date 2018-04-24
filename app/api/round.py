from flask_potion import ModelResource, fields
from app.model.Round import Round
from flask_potion.routes import Relation

class RoundResource(ModelResource):
    students = Relation('student')

    class Meta:
        model = Round

    class Schema:
        shift = fields.ToOne('shift')
