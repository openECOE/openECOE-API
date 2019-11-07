#  Copyright (c) 2019 Miguel Hernandez University of Elche
#  This file is part of openECOE-API.
#
#      openECOE-API is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      openECOE-API is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with openECOE-API.  If not, see <https://www.gnu.org/licenses/>.

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


