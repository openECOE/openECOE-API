from model import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id_user = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    is_superadmin = db.Column(db.Boolean(), default=False)


db.session.add(User(name='admin', surname='orga', is_superadmin=True))
db.session.add(User(name='user', surname='orga'))
db.session.commit()
