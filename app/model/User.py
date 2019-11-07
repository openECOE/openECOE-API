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

import os

from flask import current_app
from app import db, bcrypt
from flask_login import UserMixin

import base64
import enum
from datetime import datetime, timedelta


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    id_organization = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
    email = db.Column(db.String(255), index=True, unique=True)
    password = db.Column(db.String(255))
    registered_on = db.Column(db.DateTime)
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    is_superadmin = db.Column(db.Boolean(), nullable=False, default=False)  # TODO: Remove is_superadmin when permissions active
    token = db.Column(db.String(255), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    roles = db.relationship('Role', backref='user')
    permissions = db.relationship('Permission', backref='user')
    ecoeCoordinators = db.relationship('ECOE', backref='user')
    stationManagers = db.relationship('Station', backref='user')

    def encode_password(self, password):
        self.password = bcrypt.generate_password_hash(
            password, current_app.config['BCRYPT_LOG_ROUNDS']
        ).decode()

        db.session.commit()

    def check_password(self, candidate):
        return bcrypt.check_password_hash(
            self.password, candidate
        )

    def get_token(self, expires_in=86400):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            self.token_expiration = now + timedelta(seconds=expires_in)
            return self
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        return self

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token, expires_in=86400):
        now = datetime.utcnow()
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        user.token_expiration = now + timedelta(seconds=expires_in)
        return user


class RoleType(str, enum.Enum):
    SUPERADMIN = 'superadmin'
    ADMIN = 'administrator'
    USER = 'user'
    EVAL = 'evaluator'
    STUDENT = 'student'


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.Enum(RoleType))

    __table_args__ = (
        db.UniqueConstraint(id_user, name, name='uq_role_id_user_name'),
    )


class PermissionType(str, enum.Enum):
    MANAGE = 'manage'
    READ = 'read'


class Permission(db.Model):
    __tablename__ = 'permission'

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(255))
    id_object = db.Column(db.Integer)
    object = db.Column(db.String(255))

    __table_args__ = (
        db.UniqueConstraint(id_user, name, id_object, object, name='uq_permission_id_user_name_id_object_object'),
    )




