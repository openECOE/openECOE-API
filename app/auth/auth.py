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

from flask import g
from flask_login import current_user
from flask_principal import Identity, UserNeed, ItemNeed, AnonymousIdentity, identity_loaded, RoleNeed, TypeNeed
from flask_httpauth import HTTPTokenAuth
from werkzeug.exceptions import abort

from app import login_manager, principals
from app.model.User import User, RoleType, PermissionType

token_auth = HTTPTokenAuth()


@login_manager.request_loader
def load_user_from_request(request):
    auth_token = request.headers.get('Authorization')
    user = None

    if request.authorization:
        username, password = request.authorization.username, request.authorization.password
        user = User.check_email_password(username, password)
    elif auth_token:
        auth_token = auth_token.replace('Bearer ', '', 1)
        user = User.check_token(auth_token)

    return user


@principals.identity_loader
def read_identity_from_flask_login():
    if current_user.is_authenticated:
        return Identity(current_user.id)
    return AnonymousIdentity()


@identity_loaded.connect
def on_identity_loaded(sender, identity):
    if not isinstance(identity, AnonymousIdentity):
        identity.provides.add(UserNeed(identity.id))

        # Have permission to manage their own User
        identity.provides.add(ItemNeed(PermissionType.MANAGE, current_user.id, 'users'))
        identity.provides.add(ItemNeed(PermissionType.READ, current_user.id_organization, 'organizations'))

        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))

                # If user is ADMIN gives permission to manage all ECOEs and their organization
                if role.name == RoleType.ADMIN:
                    identity.provides.add(ItemNeed(PermissionType.MANAGE, current_user.id_organization, 'organizations'))
                    for ecoe in current_user.organization.ecoes:
                        identity.provides.add(ItemNeed(PermissionType.MANAGE, ecoe.id, 'ecoes'))

                # User SUPERADMIN obtain all roles
                if role.name == RoleType.SUPERADMIN:
                    for roleType in RoleType:
                        identity.provides.add(RoleNeed(roleType))

        if hasattr(current_user, 'permissions'):
            for permission in current_user.permissions:
                identity.provides.add(ItemNeed(permission.name, permission.id_object, permission.object))


@token_auth.verify_token
def verify_token(token):
    g.current_user = User.check_token(token) if token else None
    return g.current_user is not None


@token_auth.error_handler
def token_auth_error():
    return abort(401)
