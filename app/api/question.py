from flask_potion import ModelResource, fields
from flask_potion.routes import Relation, ItemAttributeRoute
from app.model.Question import Question, QType


class QuestionResource(ModelResource):
    options = Relation('option')
    points = ItemAttributeRoute(fields.Integer)

    class Meta:
        model = Question

    class Schema:
        area = fields.ToOne('area')
        question_type = fields.String(enum=QType)
        options = fields.ToMany('option')
        qblocks = fields.ToMany('qblock')

# TODO: Comprobar al crear una pregunta que el area y el grupo introducido pertenecen a la misma ECOE
