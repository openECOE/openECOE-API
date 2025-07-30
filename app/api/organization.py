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



from app.api.user import RoleType, PermissionType
from app.api._mainresource import OpenECOEResource
from app.model.Organization import Organization
from werkzeug.exceptions import Forbidden
#import os
#from flask import send_file, current_app



from flask_login import current_user
from flask_potion import fields
from flask_potion.routes import ItemRoute, Relation
from app.api.jobs import JobResource
from app.jobs import statistics as jobs_statistics
from app.auth import auth

class OrganizationResource(OpenECOEResource):
    users = Relation('users')
    ecoes = Relation('ecoes')

    class Meta:
        name = 'organizations'
        model = Organization
        natural_key = 'name'

        permissions = {
            'read': ['update', 'read', 'yes'],
            'create': 'delete',
            'update': ['manage', 'delete'],
            'delete': RoleType.SUPERADMIN,
            'manage': [PermissionType.MANAGE, RoleType.SUPERADMIN]
        }

    
    #Recoge los datos del trabajo
    @ItemRoute.GET("/csv")
    def get_csv_asinc_org(self, organization) -> fields.List(fields.Inline(JobResource)):
        # Only can get data if have manage permissions
        object_permissions = self.manager.get_permissions_for_item(organization)
        if "manage" in object_permissions and object_permissions["manage"] is not True:
            raise Forbidden

        item = self.manager.read(organization.id)
        job = current_user.jobs.filter_by(
            id=item.id_job_csv
        )
        
        return job

    #Genera el trabajo y lo lanza en segundo plano
    @ItemRoute.POST("/csv")
    def gen_csv_asinc_org(self, organization) -> fields.Inline(JobResource):
        # Only can get data if have manage permissions
        object_permissions = self.manager.get_permissions_for_item(organization)
        if "manage" in object_permissions and object_permissions["manage"] is not True:
            raise Forbidden

        _identidad = str(auth.current_user.id)
        _job = current_user.launch_job(
            func=jobs_statistics.export_csv,
            description="CSV_Asinc: Organization = %s" % organization.name,
            organization=str(organization.id),
            identidad=_identidad,
        )
        item = self.manager.read(organization.id)
        self.manager.update(item, {"id_job_csv": _job.id})
        return _job    