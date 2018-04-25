from model import db
from model.Student import Student
from model.Option import Option

from sqlalchemy.orm import backref


class Answer(db.Model):
    __tablename__ = 'answer'

    id_answer = db.Column(db.Integer, primary_key=True)
    id_option = db.Column(db.Integer, db.ForeignKey(Option.id_option), primary_key=True)
    option = db.relationship(Option, backref='option')
    id_student = db.Column(db.Integer, db.ForeignKey(Student.id_student), nullable=False)
    student = db.relationship(Student, backref=backref('answers', lazy='dynamic'))
