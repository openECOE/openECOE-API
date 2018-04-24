from app import db
from .Shift import Shift
from .Student import Student

from sqlalchemy.orm import backref

class Round(db.Model):
    __tablename__='round'

    id_round = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500))
    id_shift = db.Column(db.Integer, db.ForeignKey(Shift.id_shift), nullable=False)
    shift = db.relationship(Shift, backref=backref('rounds', lazy='dynamic'))
    students = db.relationship(Student, secondary='roundstu', lazy='subquery', backref=backref('rounds', lazy='dynamic'))

class RoundStudent(db.Model):
    __tablename__ = 'roundstu'

    id_round = db.Column(db.Integer, db.ForeignKey(Round.id_round), primary_key=True)
    round = db.relationship(Round, backref=backref('sturound', lazy='dynamic'))
    id_student = db.Column(db.Integer, db.ForeignKey(Student.id_student), primary_key=True)
    student = db.relationship(Student, backref=backref('sturound', lazy='dynamic'))

