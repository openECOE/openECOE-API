from sqlalchemy.orm import backref
from model import db

from model.ECOE import ECOE

class Day(db.Model):
    __tablename__ = "day"

    id_day = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    id_ecoe = db.Column(db.Integer, db.ForeignKey(ECOE.id), nullable=False)
    ecoe = db.relationship(ECOE, backref=backref('days', lazy='dynamic'))
