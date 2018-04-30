from app import db
from .many_to_many_tables import qblocks_questions


class QBlock(db.Model):
    __tablename__ = 'qblock'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    id_station = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)

    questions = db.relationship('Question', secondary=qblocks_questions, lazy=True, back_populates='qblocks')
