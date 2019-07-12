from flask_potion import fields, signals
from flask_potion.routes import Route, Relation
from flask_potion.fields import Inline
from werkzeug.exceptions import Forbidden
from datetime import datetime
from flask_login import current_user

from app.model.User import User, Role, Permission, RoleType

from flask_potion import ModelResource
from flask_potion.contrib.alchemy import SQLAlchemyManager
from flask_potion.contrib.principals import principals


class PrincipalResource(ModelResource):
    class Meta:
        manager = principals(SQLAlchemyManager)


class ForbiddenSuperadmin(Forbidden):

    """*403* `Forbidden`

    Raise if the user doesn't have the permission for the requested resource
    but was authenticated.
    """
    code = 403
    description = (
        'You don\'t have the permission to change superadmin permissions. '
        'It is either read-protected or not readable by the server.'
    )


class RoleResource(PrincipalResource):
    class Meta:
        name = 'roles'
        model = Role
        permissions = {
            'read': ['user:user', 'manage'],
            'create': 'manage',
            'update': 'manage',
            'delete': 'manage',
            'manage': ['manage',  RoleType.ADMIN]
        }

    class Schema:
        user = fields.ToOne('users')
        name = fields.String(enum=RoleType)


class PermissionResource(PrincipalResource):
    class Meta:
        name = 'permissions'
        model = Permission
        permissions = {
            'read': ['user:user', 'manage'],
            'create': 'manage',
            'update': 'manage',
            'delete': 'manage',
            'manage': ['manage', RoleType.ADMIN]
        }

    class Schema:
        user = fields.ToOne('users')


class UserResource(PrincipalResource):
    roles = Relation(RoleResource)
    permissions = Relation(PermissionResource)

    class Meta:
        name = 'users'
        model = User
        read_only_fields = ['registered_on', 'token_expiration']
        write_only_fields = ['password', 'token']
        permissions = {
            'read': 'manage',
            'create': 'manage',
            'update': 'manage',
            'delete': 'manage',
            'manage': ['manage', RoleType.ADMIN]
        }

    class Schema:
        organization = fields.ToOne('organizations')

    @Route.GET
    def me(self):
        if not current_user.is_authenticated:
            return None, 401

        return self.manager.read(current_user.id)

    me.request_schema = None
    me.response_schema = Inline('self')


@signals.before_create.connect_via(UserResource)
def on_before_create_user(sender, item):
    item.encode_password(item.password)
    item.registered_on = datetime.now()


@signals.after_update.connect_via(UserResource)
def after_update_user(sender, item, changes):
    if 'password' in changes.keys():
        item.encode_password(item.password)


@signals.before_update.connect_via(UserResource)
def before_update_user(sender, item, changes):
    # Only superadmin can change superadmin
    if 'is_superadmin' in changes.keys():
        if not current_user.is_superadmin:
            raise ForbiddenSuperadmin