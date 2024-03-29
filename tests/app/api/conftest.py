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


def resources():
    from app.api import api
    return [item for key, item in api.resources.items()]


@pytest.fixture(params=resources())
def resource(request):
    return request.param


def endpoints():
    return ["api%s" % item.route_prefix for item in resources()]


@pytest.fixture(params=endpoints())
def endpoint(request):
    return request.param