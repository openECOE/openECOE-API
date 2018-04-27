from app import db
from app.model.Chronometer import Chronometer

from sqlalchemy.orm import backref


class Alarm(db.Model):
    __tablename__ = 'alarm'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer, nullable=False)
    sound = db.Column(db.String(550), nullable=False)
    id_chronometer = db.Column(db.Integer, db.ForeignKey(Chronometer.id_chronometer), nullable=False)
    chronometer = db.relationship(Chronometer, backref=backref('alarms', lazy='dynamic'))
