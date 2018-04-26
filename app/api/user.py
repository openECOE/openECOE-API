from flask_potion import fields, signals, Api, ModelResource
from flask_potion.contrib.alchemy import SQLAlchemyManager
from flask_potion.contrib.principals import principals
from . import api
from datetime import datetime

from app.model.User import User

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


@signals.before_create.connect_via(UserResource)
def on_before_create_user(sender, item):
    item.encode_password(item.password)
    item.registered_on = datetime.now()


api.add_resource(UserResource)
