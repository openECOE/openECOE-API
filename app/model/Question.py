from app import db
from .many_to_many_tables import qblocks_questions
import enum
from sqlalchemy.ext.hybrid import hybrid_property


class QType(str, enum.Enum):
    RADIO_BUTTON = 'RB'
    CHECK_BOX = 'CH'
    RANGE_SELECT = 'RS'


class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(100))
    description = db.Column(db.String(500))
    id_area = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    question_type = db.Column(db.Enum(QType), nullable=False)

    order = db.Column(db.Integer)

    options = db.relationship('Option', backref='question')
    qblocks = db.relationship('QBlock', secondary=qblocks_questions, lazy=True, back_populates='questions')

    @hybrid_property
    def points(self):

        if self.question_type in (QType.RADIO_BUTTON, QType.RANGE_SELECT):
            return max([opt.points for opt in self.options])

        if self.question_type == QType.CHECK_BOX:
            return sum([opt.points for opt in self.options])


