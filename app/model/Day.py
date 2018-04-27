from app import db
from .many_to_many_tables import ecoes_days


class Day(db.Model):
    __tablename__ = 'day'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, unique=True)

    ecoes = db.relationship('ECOE', secondary=ecoes_days, lazy=True, back_populates='days')
    turns = db.relationship('Turn', backref='day')
