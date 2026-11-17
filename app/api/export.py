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
from flask_potion.exceptions import BadRequest

from urllib.parse import quote

import pyexcel
from flask import Response
from pyexcel.exceptions import FileTypeNotSupported


_MIME_TYPES = {
    "csv": "text/csv",
    "tsv": "text/tab-separated-values",
    "csvz": "application/zip",
    "tsvz": "application/zip",
    "ods": "application/vnd.oasis.opendocument.spreadsheet",
    "xls": "application/vnd.ms-excel",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "xlsm": "application/vnd.ms-excel.sheet.macroenabled.12",
}


def _make_response(content, file_type, file_name=None):
    """Respuesta con el fichero, como la que daba Flask-Excel (pyexcel-webio 0.1.4)."""
    if hasattr(content, "read"):
        content = content.read()
    response = Response(content, content_type=_MIME_TYPES.get(file_type, "application/octet-stream"), status=200)
    if file_name:
        if not file_name.endswith(file_type):
            file_name = "%s.%s" % (file_name, file_type)
        encoded = quote(file_name)
        response.headers["Content-Disposition"] = "attachment; filename=%s;filename*=utf-8''%s" % (encoded, encoded)
    return response


def check_filetype(decorated):
    def _filetype(*args, **kwargs):
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

    return _filetype


@check_filetype
def book_dict(_book_dict, filename, filetype):
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

    _dict = {key: query2array(items) for key, items in _book_dict.items()}
    # TODO: Investigate if it possible define sheets order for xls in make_response_from_book_dict with pyexcel.
    return _make_response(pyexcel.save_book_as(bookdict=_dict, dest_file_type=filetype), filetype, filename)


@check_filetype
def query(_query, columns, filename, filetype):
    sheet = pyexcel.get_sheet(query_sets=_query, column_names=columns)
    sheet.name = filename
    return _make_response(sheet.save_to_memory(filetype, None), filetype, filename)


@check_filetype
def dictionary(_dictionary, filename, filetype):
    return _make_response(pyexcel.save_as(adict=_dictionary, dest_file_type=filetype), filetype, filename)


@check_filetype
def records(_records, filename, filetype):
    return _make_response(pyexcel.save_as(records=_records, dest_file_type=filetype), filetype, filename)