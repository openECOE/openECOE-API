from app import db
from .ECOE import ECOE

from sqlalchemy.orm import backref


class Day(db.Model):
    __tablename__ = 'day'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    id_ecoe = db.Column(db.Integer, db.ForeignKey(ECOE.id), nullable=False)
    ecoe = db.relationship(ECOE, backref=backref('days', lazy='dynamic'))
