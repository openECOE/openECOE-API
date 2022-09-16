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

from flask_potion.routes import Relation

from app.api.user import RoleType, PermissionType
from app.api._mainresource import OpenECOEResource
from app.model.Organization import Organization
from flask_potion.routes import ItemRoute
from werkzeug.exceptions import Forbidden
import os
from flask import send_from_directory, current_app
from app.statistics import generar_csv

class OrganizationResource(OpenECOEResource):
    users = Relation('users')
    ecoes = Relation('ecoes')

    class Meta:
        name = 'organizations'
        model = Organization
        natural_key = 'name'

        permissions = {
            'read': ['update', 'read'],
            'create': 'delete',
            'update': ['manage', 'delete'],
            'delete': RoleType.SUPERADMIN,
            'manage': [PermissionType.MANAGE, RoleType.SUPERADMIN]
        }

    @ItemRoute.GET("/csv", rel='getorganization')
    def send_CSV_ecoe(self, organization):
        object_permissions = self.manager.get_permissions_for_item(organization)
        if "manage" in object_permissions and object_permissions["manage"] is not True:
            raise Forbidden
        
        file_path = os.path.join(os.path.dirname(current_app.instance_path), current_app.config.get("DEFAULT_ARCHIVE_ROUTE"))
        
        file_name = generar_csv(organization=str(organization.id))
        return send_from_directory(directory=file_path,
                                    filename=file_name,
                                    as_attachment=True)