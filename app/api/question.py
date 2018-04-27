from flask_potion import ModelResource, fields
from flask_potion.routes import Relation
from app.model.Question import Question

from app.model.Option import Option
from app.model.Answer import Answer


class QuestionResource(ModelResource):
    options = Relation('option')

    class Meta:
        model = Question

    class Schema:
        group = fields.ToOne('group')
        area = fields.ToOne('area')

# TODO: Comprobar al crear una pregunta que el area y el grupo introducido pertenecen a la misma ECOE


class OptionResource(ModelResource):
    class Meta:
        model = Option

    class Schema:
        question = fields.ToOne('question')


class AnswerResource(ModelResource):
    class Meta:
        model = Answer

    class Schema:
        student = fields.ToOne('student')
        option = fields.ToOne('option')
