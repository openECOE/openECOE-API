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

    if auth_token:
        auth_token = auth_token.replace('Bearer ', '', 1)
        user = User.check_token(auth_token)
        if user:
            return user

    if request.authorization:
        username, password = request.authorization.username, request.authorization.password

        user = User.query.filter_by(email=username).first()
        if user and user.check_password(password):
            return user
    return None


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
