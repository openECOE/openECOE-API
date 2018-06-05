from app import db
from .many_to_many_tables import students_options


class Option(db.Model):
    __tablename__ = 'option'

    id = db.Column(db.Integer, primary_key=True)
    points = db.Column(db.Numeric(10,2), nullable=False)
    label = db.Column(db.String(255))
    id_question = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    order = db.Column(db.Integer, nullable=False)

    students = db.relationship('Student', secondary=students_options, lazy=True, back_populates='answers')
