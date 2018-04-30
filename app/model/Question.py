from app import db
from .many_to_many_tables import qblocks_questions
import enum


class QType(enum.Enum):
    RADIO_BUTTON = 'RB'
    CHECK_BOX = 'CH'


class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(50))
    description = db.Column(db.String(500))
    id_area = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    type = db.Column(db.Enum(QType), nullable=False)

    answers = db.relationship('Answer', backref='question')
    options = db.relationship('Option', backref='question')
    qblocks = db.relationship('QBlock', secondary=qblocks_questions, lazy=True, back_populates='questions')
