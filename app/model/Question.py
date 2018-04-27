from app import db
from .many_to_many_tables import qblocks_questions

class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)

    reference = db.Column(db.String(50))
    description = db.Column(db.String(500))
    id_area = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    type = db.Column(db.Integer, db.ForeignKey('qtype.id'), nullable=False)

    qblocks = db.relationship('QBlock', secondary=qblocks_questions, lazy=True, back_populates='questions')
