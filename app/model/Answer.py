from app import db
from app.model.Question import Question
from app.model.Student import Student
from app.model.Option import Option

from sqlalchemy.orm import backref


class Answer(db.Model):
    __tablename__ = 'answer'

    id_answer = db.Column(db.Integer, primary_key=True)
    id_question = db.Column(db.Integer, db.ForeignKey(Question.id_question), nullable=False)
    question = db.relationship(Question, backref='question')
    id_student = db.Column(db.Integer, db.ForeignKey(Student.id_student), nullable=False)
    student = db.relationship(Student, backref=backref('answers', lazy='dynamic'))
    id_option = db.Column(db.Integer, db.ForeignKey(Option.id_option), nullable=False)
    option = db.relationship(Option, backref='option')  # TODO: relacion 1:1?
