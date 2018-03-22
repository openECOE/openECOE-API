from sqlalchemy.orm import backref
from model import db


class Day(db.Model):
    __tablename__ = "day"

    id_day = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.TIMESTAMP)
    id_ecoe = db.Column(db.Integer, db.ForeignKey('ecoe.id'), nullable=False)
    ecoe = db.relationship('ECOE', backref=backref('ecoe', lazy='dynamic'))
