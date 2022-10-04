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

from flask_potion import Resource, fields
from flask_potion.routes import  Route#, ItemRoute
import os
from flask import send_from_directory, current_app
from flask_potion.contrib.principals import principals
from werkzeug.exceptions import Forbidden
from flask_login import current_user
from app.api.jobs import JobResource
#Para llamar de forma síncrona
from app.statistics import generar_csv
#Para llamar de forma asíncrona con POST
from app.jobs import statistics as jobs_statistics
from app.auth import auth
from flask_potion.contrib.alchemy import SQLAlchemyManager
MainManager = principals(SQLAlchemyManager)

class StatisticsResource(Resource):
    
    class Schema:
        level = fields.String(enum=['info', 'warning', 'error'])
        message = fields.String()

    class Meta:
        manager = MainManager
        name = "statistics"
        natural_key = "name"
        
        permissions = {
            "read": ["manage", "read", "evaluate"],
            "manage": ["manage", "read", "evaluate"],
            "evaluate": ["manage", "read", "evaluate"]
        }

    @Route.GET("/csv", rel='getcsvcompleto')
    def send_CSV_ecoe(self):
        file_path = os.path.join(os.path.dirname(current_app.instance_path), current_app.config.get("DEFAULT_ARCHIVE_ROUTE"))
        file_name = generar_csv()
        return send_from_directory(directory=file_path,
                                    filename=file_name,
                                    as_attachment=True)

    #Recoge los datos del trabajo
    @Route.GET("/csv_asinc")
    def get__csv_asinc_ecoe(self) -> fields.List(fields.Inline(JobResource)):
        # TODO Ver como ponerle los permisos a esto, por ahora solo pueden hacerlo los superadmins
        if auth.current_user.is_superadmin is not True:
            raise Forbidden

        job = current_user.jobs.filter_by(
            name="app.jobs.statistics.export_csv(identidad=%s)" % (auth.current_user.id)
        )
        return job

    #Genera el trabajo y lo lanza en segundo plano
    @Route.POST("/csv_asinc")
    def gen__csv_asinc_ecoe(self) -> fields.Inline(JobResource):
        # TODO Ver como ponerle los permisos a esto, por ahora solo pueden hacerlo los superadmins
        if auth.current_user.is_superadmin is not True:
            raise Forbidden
        
        _identidad = str(auth.current_user.id)
        _job = current_user.launch_job(
            func=jobs_statistics.export_csv,
            description="CSV_Asinc: CSV COMPLETO",
            identidad=_identidad,
        )

        return _job      
