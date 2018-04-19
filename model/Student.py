from model import db
from sqlalchemy.orm import backref
from model.ECOE import ECOE
from model.Round import Round


class Student(db.Model):
    __tablename__ = 'student'

    id_student = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    dni = db.Column(db.String(25))
    id_ecoe = db.Column(db.Integer, db.ForeignKey(ECOE.id), nullable=False)
    ecoe = db.relationship(ECOE, backref=backref('student', lazy='dynamic'))
    id_round = db.Column(db.Integer, db.ForeignKey(Round.id_round), nullable=False)
    round = db.relationship(Round, backref=backref('student', lazy='dynamic'))
