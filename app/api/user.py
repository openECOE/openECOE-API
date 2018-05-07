from flask_potion import fields, signals, ModelResource
from flask_potion.routes import ItemRoute, Route
from flask_potion.fields import Inline
from flask_potion.contrib.alchemy import SQLAlchemyManager
from flask_potion.contrib.principals import principals
#from . import api
from datetime import datetime
from flask_login import current_user

from app.model.User import User

# TODO: check this resource file


class PrincipalResource(ModelResource):
    class Meta:
        manager = principals(SQLAlchemyManager)


class UserResource(PrincipalResource):
    class Meta:
        model = User
        write_only_fields = ['password', 'is_superadmin', 'token', 'token_expiration', 'registered_on']
        permissions = {
            'create': 'yes',
            'update': 'create',
            'delete': 'update'
        }

    @Route.GET
    def me(self):
        return self.manager.read(current_user.id)

    me.request_schema = None
    me.response_schema = Inline('self')


@signals.before_create.connect_via(UserResource)
def on_before_create_user(sender, item):
    item.encode_password(item.password)
    item.registered_on = datetime.now()
