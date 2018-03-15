from sqlalchemy.orm import backref
from ws import db
from model import ECOE

class Area(db.Model):
    __tablename__ = "area"

    id_area = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    id_ecoe = db.Column(db.Integer, db.ForeignKey(ECOE.id), nullable=False)
    ecoe = db.relationship(ECOE, backref=backref('ecoes', lazy='dynamic'))
