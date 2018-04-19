from flask_potion import Resource, fields
from flask_potion.contrib.alchemy import SQLAlchemyManager
from flask_potion.contrib.principals import principals
from flask_potion.routes import Route
from api import api
from auth import current_user

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
    def create(self, value: fields.Number()) -> fields.Inline('self'):
        return {"name": "foo", "token": value}

    @Route.GET(rel='get')
    def get_token(self) -> fields.Inline('self'):
        token = current_user.get_token()
        return {"token": token}

api.add_resource(TokenResource)
