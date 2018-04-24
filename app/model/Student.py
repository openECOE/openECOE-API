from app import db
from sqlalchemy.orm import backref
from model.ECOE import ECOE
from model.Round import Round


class Student(db.Model):
    __tablename__ = 'student'

    id_student = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    dni = db.Column(db.String(25), nullable=False, unique=True)
    id_ecoe = db.Column(db.Integer, db.ForeignKey(ECOE.id), nullable=False)
    ecoe = db.relationship(ECOE, backref=backref('students', lazy='dynamic'))
    id_round = db.Column(db.Integer, db.ForeignKey(Round.id_round))
    round = db.relationship(Round, backref=backref('students', lazy='dynamic'))
