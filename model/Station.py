from ws import db
from sqlalchemy.orm import backref
from model import Chronometer, ECOE, Stachro

class Station(db.Model):
    __tablename__ = "sta"
    id_station = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    id_ecoe = db.Column(db.Integer, db.ForeignKey("ecoe.id"), nullable=False)

    ecoe = db.relationship("ECOE", backref=backref('stations', lazy='dynamic'))
    stachro = db.relationship("Stachro")