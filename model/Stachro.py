from ws import db
from model import Chronometer, Station

class Stachro(db.Model):
    __tablename__ = "stachro"

    id_station = db.Column(db.Integer, db.ForeignKey("sta.id_station"), primary_key=True)
    id_chronometer = db.Column(db.Integer, db.ForeignKey("chro.id_chronometer"), primary_key=True)
    station = db.relationship("Station")


