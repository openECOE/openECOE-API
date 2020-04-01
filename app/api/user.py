#  Copyright (c) 2019 Miguel Hernandez University of Elche
#  This file is part of openECOE-API.
#
#      openECOE-API is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      openECOE-API is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with openECOE-API.  If not, see <https://www.gnu.org/licenses/>.

from flask_potion import fields, signals, exceptions
from flask_potion.routes import Route, Relation, ItemRoute
from flask_potion.fields import Inline

from werkzeug.exceptions import Forbidden
from datetime import datetime
from flask_login import current_user
from app.api._mainresource import OpenECOEResource


from app.model.User import User, Role, Permission, RoleType, PermissionType
from app.api.jobs import JobResource


class ForbiddenSuperadmin(Forbidden):
    description = (
        'You don\'t have the permission to change superadmin permissions. '
        'It is either read-protected or not readable by the server.'
    )


class RoleResource(OpenECOEResource):
    @Route.GET('/types')
    def roletypes(self) -> fields.String():
        roles = []

        for order, role in enumerate(RoleType, start=0):
            roles.append({"name": role, "order": order})

        return roles

    class Meta:
        name = 'roles'
        model = Role
        permissions = {
            'read': ['user:user', 'manage'],
            'create': 'manage',
            'update': 'manage',
            'delete': 'manage',
            'manage': ['manage', RoleType.ADMIN]
        }

    class Schema:
        user = fields.ToOne('users')
        name = fields.String(enum=RoleType)


class PermissionResource(OpenECOEResource):
    @Route.GET('/types')
    def permissiontypes(self) -> fields.String():
        permissions = []

        for order, permission in enumerate(PermissionType, start=0):
            permissions.append({"name": permission, "order": order})

        return permissions

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
        name = fields.String(enum=PermissionType)


class UserResource(OpenECOEResource):
    roles = Relation(RoleResource)
    permissions = Relation(PermissionResource)
    jobs = Relation('jobs')

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

    @Route.GET('/me')
    def me(self) -> fields.Inline('self'):
        if not current_user.is_authenticated:
            return None, 401

        return self.manager.read(current_user.id)


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
