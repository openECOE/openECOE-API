from ws import db
from model import Chronometer, ECOE


class ECOEChro(db.Model):
    __tablename__ = "ecoechro"

    id_ecoe = db.Column(db.Integer, db.ForeignKey("ecoe.id"), primary_key=True)
    id_chronometer = db.Column(db.Integer, db.ForeignKey("chro.id_chronometer"), primary_key=True)
    ecoe = db.relationship("ECOE")

