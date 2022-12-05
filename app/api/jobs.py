#  Copyright (c) 2020 Miguel Hernandez University of Elche
#  This file is part of openECOE-API.
#
#       openECOE-API is free software: you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation, either version 3 of the License, or
#       (at your option) any later version.
#
#       openECOE-API is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with openECOE-API.  If not, see <https://www.gnu.org/licenses/>.
import os

from flask import send_from_directory, current_app

from app.api._mainresource import OpenECOEResource
from app.model.Job import Job
from app.model.User import RoleType

from flask_potion import fields, signals
from flask_potion.routes import ItemRoute
from flask_potion.exceptions import NotFound


class JobResource(OpenECOEResource):
    class Meta:
        name = 'jobs'
        model = Job
        id_field_class = fields.String

        permissions = {
            'read': 'manage',
            'create': 'manage',
            'update': 'manage',
            'delete': 'manage',
            'manage': ['manage', RoleType.ADMIN, 'user:user']
        }

        read_only_fields = ['name', 'file', 'created', 'finished', 'complete']

    class Schema:
        user = fields.ToOne('organizations')
        progress = fields.Number()

    @ItemRoute.GET('/download')
    def get_file(self, job):
        if not job.file:
            raise NotFound(description='Not file for this job yet')

        _archiveroute = os.path.join(os.path.dirname(current_app.instance_path),
                                     current_app.config.get("DEFAULT_ARCHIVE_ROUTE"))

        return send_from_directory(directory=_archiveroute,
                                   filename=job.file,
                                   as_attachment=True)


@signals.after_delete.connect_via(JobResource)
def after_delete_job(sender, item):
    item.del_job_file()
