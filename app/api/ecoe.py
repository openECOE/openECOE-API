from flask_login import current_user
from flask_potion import fields, signals
from flask_potion.routes import Relation, ItemRoute
from app.model.ECOE import ECOE
from app import db
from .user import PrincipalResource, RoleType

# Permissions to ECOE childs resources
class EcoePrincipalResource(PrincipalResource):
    class Meta:
        permissions = {
            'read': 'read:ecoe',
            'create': 'manage',
            'update': 'manage',
            'delete': 'manage',
            'manage': 'manage:ecoe'
        }


class EcoeResource(PrincipalResource):
    areas = Relation('areas')
    stations = Relation('stations')
    schedules = Relation('schedules')
    students = Relation('students')
    rounds = Relation('rounds')
    shifts = Relation('shifts')

    @ItemRoute.GET('/configuration')
    def configuration(self, ecoe) -> fields.String():
        return ecoe.configuration

    class Meta:
        name = 'ecoes'
        model = ECOE
        natural_key = 'name'

        permissions = {
            'read': ['manage', 'read'],
            'create': 'manage',
            'update': 'manage',
            'delete': 'manage',
            'manage': ['manage', RoleType.SUPERADMIN, 'user:user']
        }

    class Schema:
        organization = fields.ToOne('organizations')
        user = fields.ToOne('users')


# # Add permissions to manage to creator
# @signals.before_create.connect_via(EcoeResource)
# def before_create_ecoe(sender, item):
#     if not hasattr(item, 'coordinator'):
#         item.coordinator = current_user.id
