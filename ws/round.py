from flask_potion import ModelResource, fields
from model.Round import Round

class RoundResource(ModelResource):

    class Meta:
        model = Round

    class Schema:
        shift = fields.ToOne('shi')
        students = fields.ToMany('stu')
        