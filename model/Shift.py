from ws import db
from model import Day
from sqlalchemy.orm import backref


class Shift(db.Model):
    __tablename__="shi"

    id_shift = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.TIME)
    id_day = db.Column(db.Integer, db.ForeignKey("day.id_day"), nullable=False)
    day = db.relationship("Day", backref=backref('shifts', lazy='dynamic'))

