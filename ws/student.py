from flask_potion import ModelResource, fields

from model.Student import Student

class StudentResource(ModelResource):
    class Meta:
        model = Student

    class Schema:
        ecoe = fields.ToOne('ecoe')
        round = fields.ToOne('round')