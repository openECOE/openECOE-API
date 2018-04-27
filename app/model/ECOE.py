from app import db
from .many_to_many_tables import ecoes_days


class ECOE(db.Model):
    __tablename__ = 'ecoe'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)

    id_org = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)

    areas = db.relationship('Area', backref='ecoe')
    chronos = db.relationship('Chronometer', backref='ecoe')
    stations = db.relationship('Station', backref='ecoe')
    students = db.relationship('Student', backref='ecoe')
    days = db.relationship('Day', secondary=ecoes_days, lazy=True, back_populates='ecoes')
    schedules = db.relationship('Schedule', backref='ecoe')


