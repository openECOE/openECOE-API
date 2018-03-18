from flask_potion import ModelResource, fields

from model.Group import Group

class GroupResource(ModelResource):
    class Meta:
        model = Group

    class Schema:
        station = fields.ToOne('sta')
