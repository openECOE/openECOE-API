from model import db
from sqlalchemy.orm import backref
from model.ECOE import ECOE

class Station(db.Model):
    __tablename__ = "sta"
    id_station = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    id_ecoe = db.Column(db.Integer, db.ForeignKey(ECOE.id), nullable=False)
    ecoe = db.relationship(ECOE, backref=backref('stations', lazy='dynamic'))

#    stachro = db.relationship("Stachro")

    def __init__(self, name='', id_ecoe='', chronometers=[]):
        self.name = name
        self.id_ecoe = id_ecoe
        self.chronometers = chronometers

    def get_station(self, id):
        station = Station.query.filter_by(id_station=id).first()
        return station

#class Stachro(db.Model):
#    __tablename__ = "stachro"

#    id_station = db.Column(db.Integer, db.ForeignKey("sta.id_station"), primary_key=True)
#    id_chronometer = db.Column(db.Integer, db.ForeignKey("chro.id_chronometer"), primary_key=True)
#    station = db.relationship("Station")


