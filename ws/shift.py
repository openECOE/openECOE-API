from flask_potion import ModelResource, fields
from flask_potion.routes import Relation

from model.Shift import Shift

class ShiftResource(ModelResource):

    class Meta:
        model = Shift

    class Schema:
        day = fields.ToOne('day')