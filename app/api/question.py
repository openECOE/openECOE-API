from flask_potion import fields
from flask_potion.routes import Relation, ItemRoute
from app.model.Question import Question, QType
from .user import PrincipalResource


class QuestionResource(PrincipalResource):
    options = Relation('options')

    @ItemRoute.GET('/points')
    def points(self, question) -> fields.Integer():
        return question.points

    class Meta:
        name = 'questions'
        model = Question

        permissions = {
            'read': 'read:area',
            'create': 'manage',
            'update': 'manage',
            'delete': 'manage',
            'manage': 'manage:area'
        }

    class Schema:
        area = fields.ToOne('areas')
        question_type = fields.String(enum=QType)
        options = fields.ToMany('options')
        qblocks = fields.ToMany('qblocks')

# TODO: Comprobar al crear una pregunta que el area y el grupo introducido pertenecen a la misma ECOE
