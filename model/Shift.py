from model import db
from sqlalchemy.orm import backref

from model.Day import Day

class Shift(db.Model):
    __tablename__ = 'shift'

    id_shift = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DATETIME)
    id_day = db.Column(db.Integer, db.ForeignKey(Day.id_day), nullable=False)
    day = db.relationship(Day, backref=backref('shifts', lazy='dynamic'))

