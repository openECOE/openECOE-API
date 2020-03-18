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

import pytest


# def pytest_generate_tests(metafunc):
#     if "endpoint" in metafunc.fixturenames:
#         from app.api import api
#         metafunc.parametrize("endpoint", _endpoints)


@pytest.mark.usefixtures('client_class')
class TestExport:

    @pytest.mark.parametrize("file_type", ['csv', 'tsv', 'csvz', 'tsvz', 'xls', 'xlsx', 'xlsm', 'ods'])
    def test_export_to_file(self, app, test_with_admin_user, endpoint, file_type):
        from pyexcel_webio import FILE_TYPE_MIME_TABLE

        endpoint += "/export?file_type=%s" % file_type
        resp = self.client.get(endpoint)
        assert resp.status_code == 200
        assert resp.content_type == FILE_TYPE_MIME_TABLE[file_type]
