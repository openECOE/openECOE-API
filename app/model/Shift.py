from app import db


class Shift(db.Model):
    __tablename__ = 'shift'

    id = db.Column(db.Integer, primary_key=True)
    shift_code = db.Column(db.String(20), nullable=False)
    id_day = db.Column(db.Integer, db.ForeignKey('day.id'), nullable=False)
    time_start = db.Column(db.String(5))  # HH:MM TODO:Review better relation with datetime or string

    wheels = db.relationship('Wheel', backref='shift')

    __table_args__ = (
        db.UniqueConstraint(shift_code, id_day, name='shift_day_uk'),
    )

