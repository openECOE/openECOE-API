from flask_potion import ModelResource, fields
from flask_potion.routes import Relation
from model.Round import Round


class RoundResource(ModelResource):
    students = Relation('student')

    class Meta:
        model = Round

    class Schema:
        shift = fields.ToOne('shift')
