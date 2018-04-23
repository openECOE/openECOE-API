from flask_potion import Resource, fields
from flask_potion.contrib.alchemy import SQLAlchemyManager
from flask_potion.contrib.principals import principals
from flask_potion.routes import Route
from flask_login import current_user
from app.api import api

api.add_resource(Resource)


class PrincipalResource(Resource):
    class Meta:
        manager = principals(SQLAlchemyManager)


class TokenResource(PrincipalResource):
    class Meta:
        name = 'token'

    class Schema:
        token = fields.String()

    @Route.POST(rel='create')
    def create_token(self) -> fields.Inline('self'):
        auth_token = current_user.encode_auth_token()
        return {"token": auth_token}

    @Route.GET(rel='get')
    def get_token(self) -> fields.Inline('self'):
        auth_token = current_user.token
        return {"token": auth_token}


api.add_resource(TokenResource)
