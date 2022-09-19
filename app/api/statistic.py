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
from flask_potion.contrib.alchemy import SQLAlchemyManager
from flask_potion.routes import  Route#, ItemRoute
import os
from flask import send_from_directory, current_app
from flask_potion.contrib.principals import principals
from app.statistics import generar_csv

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