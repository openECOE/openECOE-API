#  Copyright (c) 2019 Miguel Hernandez University of Elche
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

from flask import Flask, current_app
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_required
from flask_principal import Principal
from flask_potion import Api
from flask_cors import CORS
from config import BaseConfig
import click

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
principals = Principal()
openecoe_api = Api()
flask_app = Flask(__name__)


def create_app(config_class=BaseConfig):
    flask_app.config.from_object(config_class)

    db.init_app(flask_app)
    migrate.init_app(flask_app, db)
    login_manager.init_app(flask_app)
    bcrypt.init_app(flask_app)
    principals.init_app(flask_app)
    CORS(flask_app)

    if flask_app.config.get('API_AUTH'):
        openecoe_api.decorators.append(login_required)

    from app.auth import bp as auth_bp
    flask_app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.api import bp as api_bp
    flask_app.register_blueprint(api_bp, url_prefix='/api')

    return flask_app


@flask_app.cli.command()
@click.option('--name', prompt='Organization name', help='Organization name')
def create_orga(name):
    with current_app.app_context():
        from app.api.organization import Organization

        if Organization.query.filter_by(name=name).first():
            click.echo('Organization {} not created because exists'.format(name))
        else:
            """Create organization"""
            orga = Organization()

            orga.name = name

            db.session.add(orga)
            db.session.commit()

            click.echo('Organization {} created'.format(name))


@flask_app.cli.command()
@click.option('--email', prompt='Your email', help='User email')
@click.password_option('--password', prompt='Type password', help='User password')
@click.option('--name', help='User name')
@click.option('--surname', help='User suername')
@click.option('--admin',  is_flag=True,
              help='Flag to indicate user is admin', )
@click.option('--organization_name', default=None, help='Organization name, if not exists, create new organization')
@click.option('--organization', default=1, help='Organization to associate user (Default: 1)')
def create_user(email, password, name, surname, admin, organization, organization_name):
    with flask_app.app_context():
        from app.api.user import User, Role, RoleType
        from app.api.organization import Organization
        from datetime import datetime

        if organization_name:
            org = Organization.query.filter_by(name=organization_name).first()
            if org:
                organization = org.id
            else:
                organization = None
        else:
            org = Organization.query.filter_by(id=organization).first()
            if org:
                organization = org.id
            else:
                organization = None

        if not organization:
            click.echo('User {} not created because organization not exists'.format(email))
        elif User.query.filter_by(email=email).first():
            click.echo('User {} not created because exists in organization {}'.format(email, organization))
        else:
            """Create user"""
            user = User()
            user.registered_on = datetime.now()

            user.email = email
            user.is_superadmin = admin  # TODO: Remove superadmin RoleNeed when permissions active
            user.encode_password(password)
            user.id_organization = organization

            user.name = name
            user.surname = surname

            db.session.add(user)


            db.session.commit()

            if admin:
                role = Role()
                role.id_user = user.id
                role.name = RoleType.ADMIN
                db.session.add(role)
                db.session.commit()

            click.echo('User {} created in organization {}'.format(email, organization))


@flask_app.shell_context_processor
def make_shell_context():
    return {'db': db}
