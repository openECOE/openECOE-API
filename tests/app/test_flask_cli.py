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


@pytest.mark.usefixtures('client_class')
class Test_Create_User:
    organization = None
    organization_name = None

    def test_create_user_with_org_id(self):
        self.create_user(email='user_org_id@openecoe.es', organization=self.organization)

    def test_create_user_with_org_name(self):
        self.create_user(email='user_org_name@openecoe.es', organization_name=self.organization_name)

    def test_create_user_admin(self):
        self.create_user(email='admin@openecoe.es', admin=True)

    def __init__(self, app, make_organization):
        self.org = make_organization()
        self.runner = app.test_cli_runner()

        self.password = '1234'
        self.name = 'User'
        self.surname = 'Test'
        self.organization = self.org.id
        self.organization_name = self.org.name

    def create_user(self, email, admin=False, organization=None, organization_name=None):
        params = ['--email', email, '--password', self.password, '--name', self.name, '--surname', self.surname]

        if organization:
            params += ['--organization', organization]
        elif organization_name:
            params += ['--organization_name', organization_name]
        else:
            params += ['--organization', self.organization]

        params += ['--admin'] if admin else []

        args_ = ['create_user'] + params
        result = self.runner.invoke(args=args_)
        assert 'User {} created in organization {}'.format(email, self.organization) in result.output


def test_create_orga(app):
    runner = app.test_cli_runner()
    name = 'Testing Orga'

    # invoke the command directly
    result = runner.invoke(args=['create_orga', '--name', name])
    assert 'Organization {} created'.format(name) in result.output