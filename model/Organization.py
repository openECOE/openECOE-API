from model import db
from model.User import User


class Organization(db.Model):
    __tablename__ = 'organization'
    id_organization = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), index=True, unique=True, primary_key=True)
    # users = db.relationship('Orguser')


# class Orguser(db.Model):
#     __tablename__ = 'organization_user'
#     id_organization = db.Column(db.Integer, db.ForeignKey(Organization.id_organization), primary_key=True)
#     id_user = db.Column(db.Integer, db.ForeignKey(User.id_user), primary_key=True)
#     organization = db.relationship('Organization')