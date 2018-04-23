from app.model.User import User
from flask_principal import Principal, Identity, UserNeed, AnonymousIdentity, identity_loaded, RoleNeed
from app.auth import bp
from flask_login import current_user
from app import login, principals


@login.request_loader
def load_user_from_request(request):
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
