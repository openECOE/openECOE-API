from flask_potion import ModelResource, fields
from flask_potion.routes import Relation

from model.Question import Question

class QuestionResource(ModelResource):
    options = Relation('opt')

    class Meta:
        model = Question

    class Schema:
        group = fields.ToOne('group')
        area = fields.ToOne('area')