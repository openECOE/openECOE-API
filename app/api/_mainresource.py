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
import inspect

from flask import request, current_app
from flask_potion import ModelResource, fields
from flask_potion.exceptions import BadRequest
from flask_potion.routes import Route, ItemRoute
from flask_potion.contrib.alchemy import SQLAlchemyManager
from flask_potion.contrib.principals import principals
from werkzeug.exceptions import Forbidden

from pyexcel.exceptions import FileTypeNotSupported
from app.api import excel

MainManager = principals(SQLAlchemyManager)


class OpenECOEResource(ModelResource):
    class Decorators(object):
        @staticmethod
        def export_filetype(decorated):
            def check_filetype(*args, **kwargs):
                if "filetype" not in kwargs and len(args) <= inspect.getfullargspec(decorated).args.index('filetype'):
                    if "filetype" in request.args:
                        kwargs['filetype'] = request.args.get("filetype")
                    else:
                        kwargs['filetype'] = current_app.config.get("DEFAULT_EXPORT_FILE_TYPE")
                try:
                    return decorated(*args, **kwargs)
                except FileTypeNotSupported as e:
                    raise BadRequest(
                        description="%s File types supported %s" % (str(e), current_app.config.get("EXPORT_FILE_TYPES")))

            return check_filetype

    @staticmethod
    @Decorators.export_filetype
    def export_book_dict(dictionary, filename, filetype):
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

        _dict = {key: query2array(items) for key, items in dictionary.items()}
        # TODO: Investigate if it possible define sheets order for xls in make_response_from_book_dict with pyexcel.
        return excel.make_response_from_book_dict(adict=_dict, file_type=filetype, file_name=filename)

    @staticmethod
    @Decorators.export_filetype
    def export_query(query, columns, filename, filetype):
        return excel.make_response_from_query_sets(query_sets=query, column_names=columns,
                                                   sheet_name=filename,
                                                   file_name=filename, file_type=filetype)

    @staticmethod
    @Decorators.export_filetype
    def export_dict(dictionary, filename, filetype):
        return excel.make_response_from_dict(adict=dictionary, file_name=filename, file_type=filetype)

    @staticmethod
    @Decorators.export_filetype
    def export_records(records, filename, filetype):
        return excel.make_response_from_records(records=records, file_name=filename, file_type=filetype)

    @ItemRoute.GET('/permissions')
    def item_permissions(self, item) -> fields.String():
        object_permissions = self.manager.get_permissions_for_item(item)
        return object_permissions

    @Route.GET('/permissions')
    def object_permissions(self) -> fields.String():
        object_permissions = self.manager.get_permissions_for_item(self)
        return object_permissions

    @ItemRoute.GET('/export',
                   rel="exportItem",
                   description="export data to file")
    def item_export(self, item):
        # Only can export if have manage permissions
        object_permissions = self.manager.get_permissions_for_item(item)
        if 'manage' in object_permissions and object_permissions['manage'] is not True:
            raise Forbidden

        _filename = self.Meta.name

        _dict = {_filename: [item]}

        return self.export_book_dict(_dict, _filename)

    @Route.GET('/export',
               rel="export",
               description="export data to file")
    def object_export(self):
        # Only can export if have manage permissions
        object_permissions = self.manager.get_permissions_for_item(self)
        if 'manage' in object_permissions and object_permissions['manage'] is not True:
            raise Forbidden

        _query = self.manager.instances().all()

        _columns = self.Meta.model.__table__.columns.keys()
        _filename = self.Meta.name

        _dict = {_filename: _query}

        return self.export_book_dict(_dict, _filename)

    class Meta:
        manager = MainManager
