from flask_potion import ModelResource, fields
from flask_potion.routes import Relation
from model.Student import Student


class StudentResource(ModelResource):
    answer = Relation('answer')

    class Meta:
        model = Student
        natural_key = ('dni')

    class Schema:
        ecoe = fields.ToOne('ecoe')
        # round = fields.ToOne('round')  # TODO: hacer relación student - round
