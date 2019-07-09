from flask_potion import ModelResource, fields
from flask_potion.routes import Relation, ItemRoute
from app.model.Question import Question, QType


class QuestionResource(ModelResource):
    options = Relation('options')

    @ItemRoute.GET('/points')
    def points(self, question) -> fields.Integer():
        return question.points

    class Meta:
        name = 'questions'
        model = Question

    class Schema:
        area = fields.ToOne('areas')
        question_type = fields.String(enum=QType)
        options = fields.ToMany('options')

# TODO: Comprobar al crear una pregunta que el area y el grupo introducido pertenecen a la misma ECOE
