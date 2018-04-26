from app import db
from sqlalchemy.orm import backref

from .Day import Day


class Shift(db.Model):
    __tablename__ = 'shift'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DATETIME)
    id_day = db.Column(db.Integer, db.ForeignKey(Day.id), nullable=False)
    day = db.relationship(Day, backref=backref('shifts', lazy='dynamic'))

