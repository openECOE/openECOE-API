from flask_potion.routes import Relation

from .user import PrincipalResource, RoleType, PermissionType
from app.model.Organization import Organization


class OrganizationResource(PrincipalResource):
    users = Relation('users')
    ecoes = Relation('ecoes')

    class Meta:
        name = 'organizations'
        model = Organization
        natural_key = 'name'

        permissions = {
            'read': ['update', 'read'],
            'create': 'delete',
            'update': ['manage', 'delete'],
            'delete': RoleType.SUPERADMIN,
            'manage': [PermissionType.MANAGE, RoleType.SUPERADMIN]
        }
