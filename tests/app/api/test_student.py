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
class TestStudentClass:
    def test_api_get(self, app):
        response = self.client.get(api.prefix+"/students")
        assert response.status_code == 200


@pytest.mark.usefixtures('client_class')
class TestAnswerClass:
    def test_api_get(self):
        response = self.client.get(api.prefix+"/answers")
        assert response.status_code == 200
