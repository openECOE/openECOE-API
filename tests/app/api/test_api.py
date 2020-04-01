#  Copyright (c) 2020 Miguel Hernandez University of Elche
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

import pytest
from app.api import api


@pytest.mark.usefixtures('client_class')
class TestAPI:
    def test_schema(self, app, endpoint, test_with_admin_user):
        endpoint += '/schema#'
        resp = self.client.get(endpoint)
        assert resp.status_code == 200

    def test_get(self, app, endpoint, test_with_admin_user):
        resp = self.client.get(endpoint)
        assert resp.status_code == 200


class TestResources:
    def test_resource_permissions_defined(self, app, resource):
        assert hasattr(resource.meta, "permissions"), "attribute 'permissions' in resource.meta"
        assert 'manage' in resource.meta.permissions.keys(), "'manage' not in the permissions dict"
