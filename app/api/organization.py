from flask_potion import ModelResource
from flask_potion.routes import Relation
from flask_potion.contrib.alchemy import SQLAlchemyManager
from flask_potion.contrib.principals import principals

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
        natural_key = ('name')
        # id_attribute = 'name'
        # id_field_class = fields.String
        #include_id = True


# class OrganizationUserResource(ManagerResource):
#     class Meta:
#         model = Orguser