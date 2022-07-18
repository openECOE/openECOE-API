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

import os
import pytest

import app as flask_app
from config import TestConfig
from alembic.command import upgrade
from alembic.config import Config

basedir = os.path.abspath(os.path.dirname(__file__))
ALEMBIC_CONFIG = os.path.join(basedir, '..', 'migrations', 'alembic.ini')
pytest_plugins = ['pytest-flask-sqlalchemy']


def apply_migrations():
    """Applies all alembic migrations."""
    config = Config(ALEMBIC_CONFIG)
    upgrade(config, 'head')


def load_data(db):
    """ Create data to test """
    """ Organization """
    from app.model.Organization import Organization
    org = Organization()
    org.name = "Test Organization"
    db.session.add(org)
    db.session.flush()

    """ Users """
    from app.model.User import User, RoleType, Role
    user_admin = User()
    user_admin.id_organization = org.id
    user_admin.email = "admin@openecoe.es"
    user_admin.password = "1234567890"
    user_admin.name = "Admin"
    user_admin.surname = "openECOE"
    db.session.add(user_admin)
    db.session.flush()

    user_admin_role = Role()
    user_admin_role.id_user = user_admin.id
    user_admin_role.name = RoleType.SUPERADMIN
    db.session.add(user_admin_role)

    """ ECOE """
    from app.model.ECOE import ECOE
    ecoe1 = ECOE()
    ecoe1.name = "Test ECOE 1"
    ecoe1.id_organization = org.id
    ecoe1.id_coordinator = user_admin.id

    ecoe2 = ECOE()
    ecoe2.name = "Test ECOE 2"
    ecoe2.id_organization = org.id
    ecoe2.id_coordinator = user_admin.id

    ecoe3 = ECOE()
    ecoe3.name = "Test ECOE 3"
    ecoe3.id_organization = org.id
    ecoe3.id_coordinator = user_admin.id

    db.session.add(ecoe1)
    db.session.add(ecoe2)
    db.session.add(ecoe3)

    db.session.flush()

    """ Area """
    from app.model.Area import Area
    area1 = Area()
    area1.id_ecoe = ecoe1.id
    area1.name = 'Anamnesis'
    area1.code = '1'

    area2 = Area()
    area2.id_ecoe = ecoe1.id
    area2.name = 'Exploración física'
    area2.code = '2'

    area3 = Area()
    area3.id_ecoe = ecoe1.id
    area3.name = 'Habilidades técnicas y procedimientos'
    area3.code = '3'

    db.session.add(area1)
    db.session.add(area2)
    db.session.add(area3)

    """ Stations """
    from app.model.Station import Station
    station1 = Station()
    station1.id_ecoe = ecoe1.id
    station1.name = "TEST_E1_I_Der"
    station1.order = 1
    station1.id_manager = user_admin.id
    db.session.add(station1)

    station2 = Station()
    station2.id_ecoe = ecoe1.id
    station2.name = "TEST_E2_PE_UEI"
    station2.order = 2
    station2.id_manager = user_admin.id
    db.session.add(station2)

    station3 = Station()
    station3.id_ecoe = ecoe1.id
    station3.name = "TEST_E3_PE_Cir"
    station3.order = 3
    station3.id_manager = user_admin.id
    db.session.add(station3)
    db.session.flush()

    station4 = Station()
    station4.id_ecoe = ecoe1.id
    station4.name = "TEST_E4_EE_Cir2IC"
    station4.order = 4
    station4.id_manager = user_admin.id
    station4.id_parent_station = station3.id
    db.session.add(station4)

    station5 = Station()
    station5.id_ecoe = ecoe1.id
    station5.name = "TEST_E5_HEE_Urg"
    station5.order = 5
    station5.id_manager = user_admin.id
    db.session.add(station5)

    db.session.commit()


# Automatically enable transactions for all tests,
# without importing any extra fixtures.
@pytest.fixture(autouse=True)
def enable_transactional_tests(app, _db):
    pass


@pytest.fixture(scope='session')
def testapp(request):
    """Session-wide test `Flask` application."""
    app = flask_app.create_app(TestConfig)

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    @request.addfinalizer
    def teardown():
        ctx.pop()

    return app


@pytest.fixture(scope='session')
def _db(app, request):
    from app.model import db
    db.drop_all()
    # apply_migrations()
    db.create_all()

    load_data(db)

    # @request.addfinalizer
    # def teardown():
    #     flask_app.db.drop_all()

    return db


@pytest.fixture()
def test_with_admin_user(app):
    from app.auth import login_manager
    from app.model.User import User

    @login_manager.request_loader
    def load_user_from_request(request):
        return User.query.filter_by(email="admin@openecoe.es").first()


@pytest.fixture
def make_organization():
    from app.model.Organization import Organization

    def _make():
        org = Organization()
        org.name = 'Test Organization'

        return org

    return _make
