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
from flask import request, current_app
from flask_potion import ModelResource, fields
from flask_potion.exceptions import BadRequest
from flask_potion.routes import Route, ItemRoute
from flask_potion.contrib.alchemy import SQLAlchemyManager
from flask_potion.contrib.principals import principals

from pyexcel.exceptions import FileTypeNotSupported
from app.api import excel

MainManager = principals(SQLAlchemyManager)


class OpenECOEResource(ModelResource):
    @staticmethod
    def export_dict(dictionary, filename):
        def query2array(query):
            def row2array(row):
                d = []
                for column in row.__table__.columns:
                    d.append(str(getattr(row, column.name)))

                return d

            if len(query) == 0:
                return []

            arr = [[column.name for column in query[0].__table__.columns]]
            arr += [row2array(row) for row in query]

            return arr

        _file_type = current_app.config.get("DEFAULT_EXPORT_FILE_TYPE")
        if "file_type" in request.args:
            _file_type = request.args.get("file_type")

        try:

            _dict = {key: query2array(items) for key, items in dictionary.items()}
            _file = excel.make_response_from_book_dict(adict=_dict, file_type=_file_type, file_name=filename)
        except FileTypeNotSupported as e:
            raise BadRequest(
                description="%s File types supported ['csv','tsv','csvz', 'tsvz', 'xls', 'xlsx', 'xlsm', 'ods']" % str(
                    e))
        return _file

    @staticmethod
    def export_query(query, columns, filename):
        _file_type = current_app.config.get("DEFAULT_EXPORT_FILE_TYPE")
        if "file_type" in request.args:
            _file_type = request.args.get("file_type")

        try:
            _file = excel.make_response_from_query_sets(query_sets=query, column_names=columns,
                                                        sheet_name=filename,
                                                        file_name=filename, file_type=_file_type)
        except FileTypeNotSupported as e:
            raise BadRequest(
                description="%s File types supported ['csv','tsv','csvz', 'tsvz', 'xls', 'xlsx', 'xlsm', 'ods']" % str(
                    e))
        return _file

    @ItemRoute.GET('/permissions')
    def item_permissions(self, item) -> fields.String():
        object_permissions = self.manager.get_permissions_for_item(item)
        return object_permissions

    @Route.GET('/permissions')
    def object_permissions(self) -> fields.String():
        object_permissions = self.manager.get_permissions_for_item(self)
        return object_permissions

    @ItemRoute.GET('/export',
                   rel="export",
                   description="export data to file")
    def item_export(self, item):
        _query = [item]

        _columns = self.Meta.model.__table__.columns.keys()
        _filename = self.Meta.name

        return self.export_query(_query, _columns, _filename)

    @Route.GET('/export',
               rel="export",
               description="export data to file")
    def object_export(self):
        _query = self.manager.instances().all()

        _columns = self.Meta.model.__table__.columns.keys()
        _filename = self.Meta.name

        _dict = {_filename: _query}

        return self.export_dict(_dict, _filename)
        # return self.export_query(_query, _columns, _filename)

    class Meta:
        manager = MainManager
