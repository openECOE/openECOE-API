from ws import db
from model import Chronometer

stachro = db.Table('stachro', db.Column('id_station', db.Integer, db.ForeignKey('sta.id_station'), primary_key=True), db.Column('id_chronometer', db.Integer, db.ForeignKey('chro.id_chronometer'), primary_key=True))

class Station(db.Model):
    __tablename__ = "sta"
    id_station = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    id_ecoe = db.Column(db.Integer, db.ForeignKey('ecoe.id'))
    groups = db.relationship('Group', backref='grupos', lazy='dynamic')
    chronometers = db.relationship('Chronometer', secondary=stachro, lazy='subquery', backref=db.backref('stachro', lazy='dynamic'))

    def __init__(self, name='', id_ecoe='', chronometers=[]):
        self.name = name
        self.id_ecoe = id_ecoe
        self.chronometers = chronometers

    def get_station(self, id):
        station = Station.query.filter_by(id_estacion=id).first()
        return station

    def get_last_station(self):
        stations = Station.query.all()

        numStation = len(stations)
        station = stations[numStation-1]

        return station

    def post_station(self):
        db.session.add(self)
        db.session.commit()

    def put_station(self, name, id_ecoe):
        self.name = name
        self.id_ecoe = id_ecoe
        db.session.commit()

    def delete_station(self):
        db.session.delete(self)
        db.session.commit()

    def exist_station_groups(self, id_group):
        for group in self.groups:
            if(group.id_group==id_group):
                return True
        return False

    def exists_station_chronometer(self, id_chronometer):
        for chronometer in self.chronometers:
            if(chronometer.id_chronometer==id_chronometer):
                return True
        return False

    def put_station_chronometer(self, chronometer):
        self.chronometers.append(chronometer)
        db.session.commit()

    def delete_station_chronometer(self, chronometer):
        self.chronometers.remove(chronometer)
        db.session.commit()

