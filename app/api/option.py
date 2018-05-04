from flask_potion import ModelResource, fields
from flask_potion.routes import Relation
from app.model.Option import Option


class OptionResource(ModelResource):

    class Meta:
        model = Option

    class Schema:
        question = fields.ToOne('question')


