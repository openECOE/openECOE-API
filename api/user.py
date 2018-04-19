from blinker import ANY
from flask_potion import fields, signals, Api, ModelResource
from flask_potion.contrib.alchemy import SQLAlchemyManager
from flask_potion.contrib.principals import principals
from . import api
from werkzeug.security import generate_password_hash

from model.User import User

class PrincipalResource(ModelResource):
    class Meta:
        manager = principals(SQLAlchemyManager)


class UserResource(PrincipalResource):
    class Meta:
        model = User
        write_only_fields = ['password', 'is_superadmin', 'token', 'token_expiration']
        permissions = {
            'create': 'yes',
            'update': 'create',
            'delete': 'update'
        }


    @signals.before_create.connect_via(ANY)
    def before_create_hash_pass(sender, item):
        if issubclass(sender, UserResource):
            item.password = generate_password_hash(item.password)


api.add_resource(UserResource)
