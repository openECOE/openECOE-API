from flask import g
from flask_login import current_user
from flask_principal import Identity, UserNeed, AnonymousIdentity, identity_loaded, RoleNeed
from flask_httpauth import HTTPTokenAuth
from werkzeug.exceptions import abort

from app import login_manager, principals
from app.model.User import User

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

        if current_user.is_superadmin:
            identity.provides.add(RoleNeed('superadmin'))


@token_auth.verify_token
def verify_token(token):
    g.current_user = User.check_token(token) if token else None
    return g.current_user is not None


@token_auth.error_handler
def token_auth_error():
    return abort(401)
