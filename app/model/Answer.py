from app import db
from .many_to_many_tables import answers_options


class Answer(db.Model):
    __tablename__ = 'answer'

    id = db.Column(db.Integer, primary_key=True)
    id_question = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    id_student = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

    options = db.relationship('Option', secondary=answers_options, lazy=True, back_populates='answers')

    __table_args__ = (
        db.UniqueConstraint(id_question, id_student, name='question_student_uk'),
    )
