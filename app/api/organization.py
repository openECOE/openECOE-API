from flask_potion import ModelResource, fields
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
    class Meta:
        model = Organization
        natural_key = 'name'

    class Schema:
        users = fields.ToMany('user')
        ecoes = fields.ToMany('ecoe')


