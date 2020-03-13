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
from flask import current_app
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


# Automatically enable transactions for all tests, without importing any extra fixtures.
@pytest.fixture(autouse=True)
def enable_transactional_tests(app, _db):
    pass


@pytest.fixture(scope='session')
def app(request):
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
    # flask_app.db.app = app
    flask_app.db.drop_all()
    flask_app.db.create_all()

    @request.addfinalizer
    def teardown():
        flask_app.db.drop_all()

    return flask_app.db


@pytest.fixture
def make_organization():
    from app.model.Organization import Organization
    from app import db

    def _make():
        org = Organization()
        org.name = 'Test Organization'

        return org

    return _make
