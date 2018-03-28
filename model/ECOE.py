from sqlalchemy.orm import backref

from model import db
from model.Organization import Organization
from model.Chronometer import Chronometer
from model.Student import Student

class ECOE(db.Model):
    __tablename__ = "ecoe"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    id_organization = db.Column(db.Integer, db.ForeignKey(Organization.id_organization), nullable=False)
    organization = db.relationship(Organization, backref=backref('ecoes', lazy='dynamic'))
    chronometers = db.relationship(Chronometer, secondary="ecoechro", lazy='subquery', backref=backref('ecoes', lazy='dynamic'))
    students = db.relationship(Student, secondary="ecoestu", lazy='subquery', backref=backref('ecoes', lazy='dynamic'))

    def get_ECOE(self, id):
        ecoe = ECOE.query.filter_by(id=id).first()
        return ecoe;

class ECOEChro(db.Model):
     __tablename__ = "ecoechro"

     id_ecoe = db.Column(db.Integer, db.ForeignKey(ECOE.id), primary_key=True)
     ecoe = db.relationship(ECOE, backref=backref('ecoechro', lazy='dynamic'))
     id_chronometer = db.Column(db.Integer, db.ForeignKey(Chronometer.id_chronometer), primary_key=True)
     chronometer = db.relationship(Chronometer, backref=backref('ecoechro', lazy='dynamic'))


class ECOEStudent(db.Model):
    __tablename__ = "ecoestu"

    id_ecoe = db.Column(db.Integer, db.ForeignKey(ECOE.id), primary_key=True)
    ecoe = db.relationship(ECOE, backref=backref('ecoestu', lazy='dynamic'))
    id_student = db.Column(db.Integer, db.ForeignKey(Student.id_student), primary_key=True)
    student = db.relationship(Student, backref=backref('ecoestu', lazy='dynamic'))