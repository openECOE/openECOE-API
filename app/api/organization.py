from flask_potion import ModelResource, fields
from flask_potion.routes import Relation
from flask_potion.contrib.alchemy import SQLAlchemyManager
from flask_potion.contrib.principals import principals
from . import api

from app.model.Organization import Organization


class ManagerResource(ModelResource):
    class Meta:
        manager = principals(SQLAlchemyManager)
        permissions = {
            'create': 'yes',
            'update': 'create',
            'delete': 'update'
        }


class OrganizationResource(ManagerResource):
    ecoes = Relation('ecoe')

    class Meta:
        model = Organization
        # id_attribute = 'name'
        # id_field_class = fields.String
        #include_id = True


# class OrganizationUserResource(ManagerResource):
#     class Meta:
#         model = Orguser


api.add_resource(OrganizationResource)
# api.add_resource(OrganizationUserResource)
