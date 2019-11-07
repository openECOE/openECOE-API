#  Copyright (c) 2019 Miguel Hernandez University of Elche
#  This file is part of openECOE-API.
#
#      openECOE-API is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      openECOE-API is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with openECOE-API.  If not, see <https://www.gnu.org/licenses/>.

from flask_login import current_user
from flask_potion import fields, signals
from flask_potion.routes import Relation, ItemRoute
from app.model.ECOE import ECOE
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
            'create': 'update',
            'update': [RoleType.ADMIN, 'manage'],
            'delete': 'manage',
            'manage': ['manage', RoleType.SUPERADMIN, 'user:user']
        }

    class Schema:
        organization = fields.ToOne('organizations', nullable=True)
        user = fields.ToOne('users', nullable=True)


# Add permissions to manage to creator
@signals.before_create.connect_via(EcoeResource)
def before_create_ecoe(sender, item):
    if not item.organization:
        item.organization = current_user.organization

    if not item.user:
        item.user = current_user
