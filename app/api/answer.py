from flask_potion import ModelResource, fields
from flask_potion.routes import Relation
from app.model.Answer import Answer


class AnswerResource(ModelResource):
    options = Relation('option')

    class Meta:
        model = Answer
        natural_key = ('question', 'student')

    class Schema:
        question = fields.ToOne('question')
        student = fields.ToOne('student')

