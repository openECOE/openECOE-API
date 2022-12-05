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
import os
from flask import send_file, current_app
from app.statistics import generar_csv


from flask_login import current_user
from flask_potion import fields
from flask_potion.routes import ItemRoute, Relation
from app.api.jobs import JobResource
from app.jobs import statistics as jobs_statistics
from app.auth import auth

class OrganizationResource(OpenECOEResource):
    organizations = Relation('organizations')
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
        import tempfile
        object_permissions = self.manager.get_permissions_for_item(organization)
        if "manage" in object_permissions and object_permissions["manage"] is not True:
            raise Forbidden
        
        file_path = os.path.join(os.path.dirname(current_app.instance_path), current_app.config.get("DEFAULT_ARCHIVE_ROUTE"))
        
        file_name = generar_csv(organization=str(organization.id))
        
        with open(file_path + "/" + file_name, mode='rb') as file: # b is important -> binary
            fileContent = file.read(-1)

        os.remove(os.path.join(file_path, file_name))
         
        ficherotemporal=tempfile.TemporaryFile()
        
        ficherotemporal.write(fileContent)
        
        ficherotemporal.seek(0)
        
        return send_file(filename_or_fp = ficherotemporal,
                                attachment_filename=file_name,
                                as_attachment=True)
    
    #Recoge los datos del trabajo
    @ItemRoute.GET("/csv_asinc")
    def get_csv_asinc_org(self, organization) -> fields.List(fields.Inline(JobResource)):
        # Only can get data if have manage permissions
        object_permissions = self.manager.get_permissions_for_item(organization)
        if "manage" in object_permissions and object_permissions["manage"] is not True:
            raise Forbidden

        job = current_user.jobs.filter_by(
            #TODO:: Esto es una función customizada que se gestiona en el módulo jobs, cambiar la ruta al 
            name="app.jobs.statistics.export_csv(organization=%s, identidad=%s)" % (organization.id, auth.current_user.id)
        )
        return job

    #Genera el trabajo y lo lanza en segundo plano
    @ItemRoute.POST("/csv_asinc")
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

        return _job    