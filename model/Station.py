from model import db
from sqlalchemy.orm import backref
from model.ECOE import ECOE
from model.Chronometer import Chronometer


class Station(db.Model):
    __tablename__ = 'station'
    id_station = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    id_ecoe = db.Column(db.Integer, db.ForeignKey(ECOE.id), nullable=False)
    ecoe = db.relationship(ECOE, backref=backref('stations', lazy='dynamic'))
    chronometers = db.relationship(Chronometer, secondary='station_chrono', lazy='subquery', backref=backref('stations', lazy='dynamic'))

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
    __tablename__ = 'station_chrono'

    id_station = db.Column(db.Integer, db.ForeignKey(Station.id_station), primary_key=True)
    id_chronometer = db.Column(db.Integer, db.ForeignKey(Chronometer.id_chronometer), primary_key=True)
    station = db.relationship(Station, backref=backref('station_chrono', lazy='dynamic'))
    chronometer = db.relationship(Chronometer, backref=backref('station_chrono', lazy='dynamic'))
