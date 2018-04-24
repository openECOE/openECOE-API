from flask_potion import ModelResource, fields
from flask_potion.routes import Relation

from app.model.Student import Student

class StudentResource(ModelResource):
    answer = Relation('answer')

    class Meta:
        model = Student

    class Schema:
        ecoe = fields.ToOne('ecoe')
        # round = fields.ToOne('round')  # TODO: hacer relación student - round
