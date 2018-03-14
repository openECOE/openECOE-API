from ws import db
from sqlalchemy.orm import backref

from model import Round, ECOE

class Student(db.Model):
    __tablename__="stu"

    id_student = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    dni = db.Column(db.String(25))
    id_ecoe = db.Column(db.Integer, db.ForeignKey(ECOE.id), nullable=False)
    ecoe = db.relationship("ECOE", backref=backref('studentsecoe', lazy='dynamic'))
    id_round = db.Column(db.Integer, db.ForeignKey(Round.id_round))
    round = db.relationship("Round", backref=backref('studentsround', lazy='dynamic'))

