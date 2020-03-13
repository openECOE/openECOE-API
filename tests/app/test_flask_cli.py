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


def test_create_orga(app):
    runner = app.test_cli_runner()
    name = 'Testing Orga'

    # invoke the command directly
    result = runner.invoke(args=['create_orga', '--name', name])
    assert 'Organization {} created'.format(name) in result.output


@pytest.mark.usefixtures('client_class')
class TestCreateUser:
    @pytest.fixture(autouse=True)
    def _init_user_test(self, app, make_organization):
        self.org = make_organization()
        self.org.name = 'Org Create User'
        self.runner = app.test_cli_runner()

        self.email = 'user@openecoe.es'
        self.password = '1234'
        self.name = 'User'
        self.surname = 'Test'

    @pytest.mark.parametrize("admin", [True, False])
    @pytest.mark.parametrize("with_org_name", [True, False])
    def test_create_user(self, db_session, admin, with_org_name):
        db_session.add(self.org)
        db_session.commit()

        params = ['--email', self.email, '--password', self.password, '--name', self.name, '--surname', self.surname]

        if with_org_name:
            params += ['--organization_name', self.org.name]
        else:
            params += ['--organization', self.org.id]

        params += ['--admin'] if admin else []

        args_ = ['create_user'] + params
        result = self.runner.invoke(args=args_)
        assert 'User {} created in organization {}'.format(self.email, self.org.id) in result.output

