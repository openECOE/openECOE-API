from flask_potion import ModelResource, fields
from app.model.Student import Student


class StudentResource(ModelResource):
    class Meta:
        model = Student

    class Schema:
        ecoe = fields.ToOne('ecoe')
        wheel = fields.ToOne('wheel')
        answers = fields.ToMany('answer')


