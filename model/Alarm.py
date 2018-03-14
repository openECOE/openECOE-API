from ws import db
from sqlalchemy.orm import backref

from model import Chronometer


class Alarm(db.Model):
    __tablename__= "ala"

    id_alarm = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)
    sound = db.Column(db.String(550))
    id_chronometer = db.Column(db.Integer, db.ForeignKey("chro.id_chronometer"), nullable=False)
    chronometer = db.relationship("Chronometer", backref=backref('alarms', lazy='dynamic'))