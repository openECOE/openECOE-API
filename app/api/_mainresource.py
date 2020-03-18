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
from flask import request
from flask_potion import ModelResource, exceptions, fields
from flask_potion.routes import Route, ItemRoute
from flask_potion.contrib.alchemy import SQLAlchemyManager
from flask_potion.contrib.principals import principals

from pyexcel import exceptions as pyexcel_exc
from app.api import excel

MainManager = principals(SQLAlchemyManager)


class OpenECOEResource(ModelResource):
    @ItemRoute.GET('/permissions')
    def item_permissions(self, item) -> fields.String():
        object_permissions = self.manager.get_permissions_for_item(item)
        return object_permissions

    @Route.GET('/permissions')
    def object_permissions(self) -> fields.String():
        object_permissions = self.manager.get_permissions_for_item(self)
        return object_permissions

    _export_schema = {
        "type": "object",
        "properties": {
            "file_type": {
                "default": "xls",
                "type": ["string", "null"],
                "anyOf": ['csv', 'tsv', 'csvz', 'tsvz', 'xls', 'xlsx', 'xlsm', 'ods']
            }
        }
    }

    @Route.GET('/export',
               rel="exportData",
               description="export data to file")
    def export(self):
        _file_type = "xls"
        if "file_type" in request.args:
            _file_type = request.args.get("file_type")

        _query = self.manager.instances().all()

        _columns = self.Meta.model.__table__.columns.keys()
        _filename = _sheet_name = self.Meta.name
        try:
            _file = excel.make_response_from_query_sets(query_sets=_query, column_names=_columns,
                                                        sheet_name=_sheet_name,
                                                        file_name=_filename, file_type=_file_type)
        except pyexcel_exc.FileTypeNotSupported as e:
            raise exceptions.BadRequest(
                description="%s File types supported ['csv','tsv','csvz', 'tsvz', 'xls', 'xlsx', 'xlsm', 'ods']" % str(
                    e))
        return _file

    class Meta:
        manager = MainManager
