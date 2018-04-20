from flask_login import LoginManager, current_user, login_required
from start import app
from model.User import User
from flask_principal import Principal, Identity, UserNeed, AnonymousIdentity, identity_loaded, RoleNeed

login_manager = LoginManager(app)


@login_manager.request_loader
def load_user_from_request(request):
    if request.authorization:
        email, password = request.authorization.username, request.authorization.password

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return user
    return None


principals = Principal(app)


@principals.identity_loader
def read_identity_from_flask_login():
    if current_user.is_authenticated:
        return Identity(current_user.id_user)
    return AnonymousIdentity()


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    if not isinstance(identity, AnonymousIdentity):
        identity.provides.add(UserNeed(identity.id))

        if current_user.is_superadmin:
            identity.provides.add(RoleNeed('superadmin'))

