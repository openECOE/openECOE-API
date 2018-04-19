from model import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import base64
from datetime import datetime, timedelta
import os


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id_user = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    password = db.Column(db.String(128))
    is_superadmin = db.Column(db.Boolean(), default=False)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user


# db.session.add(User(name='admin', surname='orga', is_superadmin=True))
# db.session.add(User(name='user', surname='orga'))
# db.session.commit()