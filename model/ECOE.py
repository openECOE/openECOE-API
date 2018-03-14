from sqlalchemy.orm import backref

from ws import db
from model import Chronometer, Organization, ECOEChro

class ECOE(db.Model):
    __tablename__ = "ecoe"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    id_organization = db.Column(db.Integer, db.ForeignKey("org.id_organization"), nullable=False)
    organization = db.relationship("Organization", backref=backref('orgs', lazy='dynamic'))
    ecoechro = db.relationship("ECOEChro")

