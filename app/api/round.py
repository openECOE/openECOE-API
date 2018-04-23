from flask_potion import ModelResource, fields
from app.model.Round import Round

class RoundResource(ModelResource):

    class Meta:
        model = Round

    class Schema:
        shift = fields.ToOne('shift')
        students = fields.ToMany('student')
