from app import db
from sqlalchemy.orm import backref
from .Group import Group
from .Area import Area


class Question(db.Model):
    __tablename__ = 'question'

    id_question = db.Column(db.Integer, primary_key=True)
    id_group = db.Column(db.Integer, db.ForeignKey(Group.id_group), nullable=False)
    group = db.relationship(Group, backref=backref('questions', lazy='dynamic'))
    id_area = db.Column(db.Integer, db.ForeignKey(Area.id_area), nullable=False)
    area = db.relationship(Area, backref='area')  # Esta relación no debe de ser inversa
    wording = db.Column(db.String(500))
    option_type = db.Column(db.String(255))

    def __init__(self, wording='', option_type='', id_group=0, id_area=0):
        self.wording = wording
        self.option_type = option_type
        self.id_group = id_group
        self.id_area = id_area

    def get_last_ques(self):
        questions = Question.query.all()

        numquestions = len(questions)
        question = questions[numquestions-1]

        return question

    def get_question(self, id):
        question = Question.query.filter_by(id_question=id).first()
        return question

    def post_question(self):
        db.session.add(self)
        db.session.commit()

    def path_question(self, newQuestion):
        self.wording = newQuestion.wording
        self.option_type = newQuestion.option_type
        self.id_group = newQuestion.id_group
        self.id_area = newQuestion.id_area

        db.session.commit()
