from flask_potion import ModelResource, fields
from app.model.Option import Option


class OptionResource(ModelResource):

    class Meta:
        name = 'options'
        model = Option

    class Schema:
        question = fields.ToOne('questions')

