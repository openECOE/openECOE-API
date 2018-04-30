from app import db
import enum


class ShiftType(enum.Enum):
    MORNING = "M"
    AFTERNOON = "T"


class Shift(db.Model):
    __tablename__ = 'shift'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Enum(ShiftType), nullable=False)
    id_day = db.Column(db.Integer, db.ForeignKey('day.id'), nullable=False)
    time_start = db.Column(db.String(5))  # HH:MM

    wheels = db.relationship('Wheel', backref='shift')

    __table_args__ = (
        db.UniqueConstraint(code, id_day, name='shift_day_uk'),
    )

