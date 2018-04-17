from flask_potion import ModelResource
from flask_potion.routes import Relation
from flask_potion.contrib.alchemy import SQLAlchemyManager
from flask_potion.contrib.principals import principals
from . import api

from model.Organization import Organization, Orguser

class ManagerResource(ModelResource):
    class Meta:
        manager = principals(SQLAlchemyManager)
        permissions = {
            'create': 'superadmin',
            'update': 'create',
            'delete': 'update'
        }


class OrganizationResource(ManagerResource):
    ecoes = Relation('ecoe')

    class Meta:
        model = Organization


class OrganizationUserResource(ManagerResource):
    class Meta:
        model = Orguser


api.add_resource(OrganizationResource)
api.add_resource(OrganizationUserResource)
