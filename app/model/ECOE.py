from sqlalchemy.orm import backref

from app import db
from app.model.Organization import Organization
from app.model.Chronometer import Chronometer


class ECOE(db.Model):
    __tablename__ = 'ecoe'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    id_organization = db.Column(db.Integer, db.ForeignKey(Organization.id_organization), nullable=False)
    organization = db.relationship(Organization, backref=backref('ecoes', lazy='dynamic'))
    chronometers = db.relationship(Chronometer, secondary='ecoe_chrono', lazy='subquery', backref=backref('ecoes', lazy='dynamic'))


class ECOEChro(db.Model):
     __tablename__ = 'ecoe_chrono'

     id_ecoe = db.Column(db.Integer, db.ForeignKey(ECOE.id), primary_key=True)
     ecoe = db.relationship(ECOE, backref=backref('ecoe_chrono', lazy='dynamic'))
     id_chronometer = db.Column(db.Integer, db.ForeignKey(Chronometer.id_chronometer), primary_key=True)
     chronometer = db.relationship(Chronometer, backref=backref('ecoe_chrono', lazy='dynamic'))


# class ECOEStudent(db.Model):
#     __tablename__ = 'ecoe_student'
#
#     id_ecoe = db.Column(db.Integer, db.ForeignKey(ECOE.id), primary_key=True)
#     ecoe = db.relationship(ECOE, backref=backref('ecoe_student', lazy='dynamic'))
#     id_student = db.Column(db.Integer, db.ForeignKey(Student.id), primary_key=True)
#     student = db.relationship(Student, backref=backref('ecoe_student', lazy='dynamic'))
