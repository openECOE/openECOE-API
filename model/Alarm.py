from model import db
from sqlalchemy.orm import backref

from model.Chronometer import Chronometer


class Alarm(db.Model):
    __tablename__= "ala"

    id_alarm = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer, nullable=False)
    sound = db.Column(db.String(550), nullable=False)
    id_chronometer = db.Column(db.Integer, db.ForeignKey(Chronometer.id_chronometer), nullable=False)
    chronometer = db.relationship(Chronometer, backref=backref('alarms', lazy='dynamic'))