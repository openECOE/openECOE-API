from flask_potion import fields, signals, Api, ModelResource
from flask_potion.contrib.alchemy import SQLAlchemyManager
from flask_potion.contrib.principals import principals
from . import api

from model.User import User
from model import db


class PrincipalResource(ModelResource):
    class Meta:
        manager = principals(SQLAlchemyManager)


class UserResource(PrincipalResource):
    class Meta:
        model = User


api.add_resource(UserResource)