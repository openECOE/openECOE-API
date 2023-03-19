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

import logging
import os
from logging.handlers import RotatingFileHandler

import click
from flask import Flask, current_app, request, url_for
from flask_cors import CORS
from flask_socketio import SocketIO

from werkzeug.middleware.proxy_fix import ProxyFix

from config import BaseConfig

flask_app = Flask(__name__)
flask_app.config.from_object(BaseConfig)

socketio = SocketIO(logger=True, engineio_logger=True, async_mode='eventlet')

def create_app(config_class=BaseConfig):
    flask_app.config.from_object(config_class)
    CORS(flask_app)

    from app.status import bp as status_bp

    status_bp.url_prefix = "/status"
    flask_app.register_blueprint(status_bp)

    from app.auth import bp as auth_bp

    auth_bp.url_prefix = "/auth"
    flask_app.register_blueprint(auth_bp)

    from app.api import bp as api_bp

    api_bp.url_prefix = "/api"
    flask_app.register_blueprint(api_bp)
    
    from app.chrono import bp as chrono_bp

    chrono_bp.url_prefix = "/chrono"
    flask_app.register_blueprint(chrono_bp)
    
    if not flask_app.debug and not flask_app.testing:
        if flask_app.config["LOG_TO_STDOUT"]:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            flask_app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists("logs"):
                os.mkdir("logs")
            file_handler = RotatingFileHandler(
                "logs/openecoe-api.log", maxBytes=10240, backupCount=10
            )
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)s: %(message)s "
                    "[in %(pathname)s:%(lineno)d]"
                )
            )
            file_handler.setLevel(logging.INFO)
            flask_app.logger.addHandler(file_handler)

        flask_app.logger.setLevel(logging.INFO)
        flask_app.logger.info("openECOE-API startup")

    socketio.init_app(flask_app)
    return flask_app


@flask_app.cli.command()
@click.option("--name", prompt="Organization name", help="Organization name")
def create_orga(name):
    with current_app.app_context():
        from app.api.organization import Organization
        from app.model import db

        if Organization.query.filter_by(name=name).first():
            click.echo("Organization {} not created because exists".format(name))
        else:
            """Create organization"""
            orga = Organization()

            orga.name = name

            db.session.add(orga)
            db.session.commit()

            click.echo("Organization {} created".format(name))


@flask_app.cli.command()
@click.option("--email", prompt="Your email", help="User email")
@click.password_option("--password", prompt="Type password", help="User password")
@click.option("--name", help="User name")
@click.option("--surname", help="User suername")
@click.option(
    "--admin",
    is_flag=True,
    help="Flag to indicate user is admin",
)
@click.option(
    "--organization_name",
    default=None,
    help="Organization name, if not exists, create new organization",
)
@click.option(
    "--organization", default=1, help="Organization to associate user (Default: 1)"
)
def create_user(email, password, name, surname, admin, organization, organization_name):
    with flask_app.app_context():
        from datetime import datetime

        from app.api.organization import Organization
        from app.api.user import Role, RoleType, User
        from app.model import db

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
            click.echo(
                "User {} not created because organization not exists".format(email)
            )
        elif User.query.filter_by(email=email).first():
            click.echo(
                "User {} not created because exists in organization {}".format(
                    email, organization
                )
            )
        else:
            """Create user"""
            user = User()
            user.registered_on = datetime.now()

            user.email = email
            user.is_superadmin = (
                admin  # TODO: Remove superadmin RoleNeed when permissions active
            )
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

@flask_app.cli.command()
def virgin():
    with current_app.app_context():
        from app.api.organization import Organization
        from app.model import db
        import sys

        count = db.session.query(Organization).count()
        click.echo('Number of organizations: {}'.format(count))
        sys.exit(count)
