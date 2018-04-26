from flask_potion import ModelResource, fields

from app.model.Area import Area


class AreaResource(ModelResource):
    class Meta:
        model = Area
        natural_key = ('name')

    class Schema:
        ecoe = fields.ToOne('ecoe')
