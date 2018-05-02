from flask_potion import ModelResource, fields
from app.model.Answer import Answer


class AnswerResource(ModelResource):
    class Meta:
        model = Answer
        natural_key = ('id_question', 'id_student')

    class Schema:
        question = fields.ToOne('question')
        student = fields.ToOne('student')
        options = fields.ToMany('option')
