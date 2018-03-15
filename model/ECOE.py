from sqlalchemy.orm import backref

from ws import db
from model.Organization import Organization
from model.Chronometer import Chronometer

class ECOE(db.Model):
    __tablename__ = "ecoe"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    id_organization = db.Column(db.Integer, db.ForeignKey(Organization.id_organization), nullable=False)
    organization = db.relationship(Organization, backref=backref('ecoes', lazy='dynamic'))


class ECOEChro(db.Model):
    __tablename__ = "ecoechro"

    id_ecoe = db.Column(db.Integer, db.ForeignKey(ECOE.id), primary_key=True)
    id_chronometer = db.Column(db.Integer, db.ForeignKey(Chronometer.id_chronometer), primary_key=True)
    ecoe = db.relationship(ECOE, backref=backref('chronos', lazy='dynamic'))
