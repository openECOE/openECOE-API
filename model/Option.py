from ws import db
from model import Question

from sqlalchemy.orm import backref

class Option(db.Model):
    __tablename__ = "opt"

    id_option = db.Column(db.Integer, primary_key=True)
    points = db.Column(db.Integer)
    description = db.Column(db.String(255))
    id_questions = db.Column(db.Integer, db.ForeignKey("ques.id_question"), nullable=False)
    question = db.relationship("Question", backref=backref('options', lazy='dynamic'))
