from flask_potion import ModelResource, fields
from flask_potion.contrib.alchemy import SQLAlchemyManager
from flask_potion.contrib.principals import principals
from flask_potion.routes import Relation

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
    users = Relation('user')
    ecoes = Relation('ecoe')

    class Meta:
        model = Organization
        natural_key = 'name'



