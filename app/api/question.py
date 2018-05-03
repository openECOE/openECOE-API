from flask_potion import ModelResource, fields
from flask_potion.routes import Relation
from app.model.Question import Question


class QuestionResource(ModelResource):
    answers = Relation('answer')
    options = Relation('option')
    # qblocks = Relation('qblock')

    class Meta:
        model = Question

    class Schema:
        area = fields.ToOne('area')


# TODO: Comprobar al crear una pregunta que el area y el grupo introducido pertenecen a la misma ECOE
