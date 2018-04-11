from flask_potion import ModelResource
from flask_potion.routes import Relation
from flask_potion.contrib.alchemy import SQLAlchemyManager
from flask_potion.contrib.principals import principals

from model.Organization import Organization

class OrganizationResource(ModelResource):
    ecoes = Relation('ecoe')

    class Meta:
        manager = principals(SQLAlchemyManager)
        model = Organization
        permissions = {
            'create': 'superadmin',
            'update': 'create',
            'delete': 'update'
        }
