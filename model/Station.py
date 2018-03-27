from model import db
from sqlalchemy.orm import backref
from model.ECOE import ECOE
from model.Chronometer import Chronometer

class Station(db.Model):
    __tablename__ = "sta"
    id_station = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    id_ecoe = db.Column(db.Integer, db.ForeignKey(ECOE.id), nullable=False)
    ecoe = db.relationship(ECOE, backref=backref('stations', lazy='dynamic'))

    chronometers = db.relationship(Chronometer, secondary="stachro", lazy='subquery', backref=backref('stations', lazy='dynamic'))


    def __init__(self, name='', id_ecoe='', chronometers=[]):
        self.name = name
        self.id_ecoe = id_ecoe
        self.chronometers = chronometers

    def get_station(self, id):
        station = Station.query.filter_by(id_station=id).first()
        return station

    def get_stations(self):
        stations = Station.query.all()

        return stations


class Stachro(db.Model):
    __tablename__ = "stachro"

    id_station = db.Column(db.Integer, db.ForeignKey("sta.id_station"), primary_key=True)
    id_chronometer = db.Column(db.Integer, db.ForeignKey("chro.id_chronometer"), primary_key=True)
    station = db.relationship(Station, backref=backref('stachro', lazy='dynamic'))
    chronometer = db.relationship(Chronometer, backref=backref('stachro', lazy='dynamic'))