from flask_potion import ModelResource, fields
from app.model.Question import Question


class QuestionResource(ModelResource):
    class Meta:
        model = Question

    class Schema:
        area = fields.ToOne('area')
        answers = fields.ToMany('answer')
        options = fields.ToMany('option')
        qblocks = fields.ToMany('qblock')

# TODO: Comprobar al crear una pregunta que el area y el grupo introducido pertenecen a la misma ECOE
