from flask_potion.routes import Relation

from .user import PrincipalResource, RoleType
from app.model.Organization import Organization


class OrganizationResource(PrincipalResource):
    users = Relation('users')
    ecoes = Relation('ecoes')

    class Meta:
        name = 'organizations'
        model = Organization
        natural_key = 'name'

        permissions = {
            'read': ['manage', 'read'],
            'create': 'manage',
            'update': 'manage',
            'delete': 'manage',
            'manage': RoleType.SUPERADMIN
        }



