from flask_potion import ModelResource, fields
from flask_potion.routes import Relation
from model.Group import Group


class GroupResource(ModelResource):
    questions = Relation('question')

    class Meta:
        model = Group

    class Schema:
        station = fields.ToOne('station')
