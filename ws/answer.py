from flask_potion import ModelResource, fields
from model.Answer import Answer


class AnswerResource(ModelResource):

    class Meta:
        model = Answer

    class Schema:
        student = fields.ToOne('student')
        question = fields.ToOne('question')
        option = fields.ToOne('option')
