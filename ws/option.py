from flask_potion import ModelResource, fields
from model.Option import Option


class OptionResource(ModelResource):
    class Meta:
        model = Option

    class Schema:
        question = fields.ToOne('question')
