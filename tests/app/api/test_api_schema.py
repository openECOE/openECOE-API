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
class Test_API:
    def test_schema(self, app):
        response = self.client.get(api.prefix + "/schema#")
        print("Test API schema works")
        assert response.status_code == 200, "API schema works"
        print("key properties is present")
        assert 'properties' in response.json.keys(), "key properties is present"

        for key, item in response.json['properties'].items():
            resp = self.client.get(item['$ref'])
            print("Test %s Schema works" % key)
            assert resp.status_code == 200
