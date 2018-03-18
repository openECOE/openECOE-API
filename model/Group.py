from model import db
from model.Station import Station

from sqlalchemy.orm import backref

class Group(db.Model):
    __tablename__ = "group"
    id_group = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    id_station = db.Column(db.Integer, db.ForeignKey(Station.id_station), nullable=False)
    station = db.relationship(Station, backref=backref('groups', lazy='dynamic'))