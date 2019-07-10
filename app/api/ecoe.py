from flask_login import current_user
from flask_potion import fields, signals
from flask_potion.routes import Relation, ItemRoute
from app.model.ECOE import ECOE
from app import db
from .user import PrincipalResource, RoleType
from app.model.User import Permission


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
            'read': 'manage',
            'create': 'manage',
            'update': 'manage',
            'delete': 'manage',
            'manage': ['manage', RoleType.ADMIN]
        }

    class Schema:
        organization = fields.ToOne('organizations')


# Add permissions to manage to creator
@signals.after_create.connect_via(EcoeResource)
def after_create_ecoe(sender, item):

    permission = Permission()

    permission.id_user = current_user.id
    permission.name = 'manage'
    permission.id_object = item.id
    permission.object = 'ecoes'

    db.session.add(permission)
    db.session.commit()

