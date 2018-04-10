from flask_potion import ModelResource
from flask_potion.routes import Relation

from model.Student import Student

class StudentResource(ModelResource):
    ecoes = Relation('ecoe')
    rounds = Relation('round')

    class Meta:
        model = Student

