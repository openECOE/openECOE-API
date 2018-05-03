from flask_potion import ModelResource, fields
from flask_potion.routes import Relation
from app.model.Student import Student


class StudentResource(ModelResource):
    answers = Relation('answer')

    class Meta:
        model = Student

    class Schema:
        ecoe = fields.ToOne('ecoe')
        wheel = fields.ToOne('wheel')



