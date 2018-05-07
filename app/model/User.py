import os

from flask import current_app
from app import db, bcrypt
from flask_login import UserMixin

import base64
from datetime import datetime, timedelta

# TODO: check this file


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), index=True, unique=True)
    password = db.Column(db.String(255))
    registered_on = db.Column(db.DateTime)
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    is_superadmin = db.Column(db.Boolean(), nullable=False, default=False)
    token = db.Column(db.String(255), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    id_organization = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)

    def encode_password(self, password):
        self.password = bcrypt.generate_password_hash(
            password, current_app.config['BCRYPT_LOG_ROUNDS']
        ).decode()

    def check_password(self, candidate):
        return bcrypt.check_password_hash(
            self.password, candidate
        )

    def get_token(self, expires_in=3600):
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
    def check_token(token, expires_in=3600):
        now = datetime.utcnow()
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        user.token_expiration = now + timedelta(seconds=expires_in)
        return user
