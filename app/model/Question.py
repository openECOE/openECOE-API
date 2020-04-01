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
from sqlalchemy.dialects import mysql


class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    id_area = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    id_station = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    id_block = db.Column(db.Integer, db.ForeignKey('block.id'))
    question_schema = db.Column(mysql.LONGTEXT(), nullable=False)
    max_points = db.Column(db.DECIMAL(precision=10, scale=2), nullable=False)

    answers = db.relationship('Answer', backref='question')


class Block(db.Model):
    __tablename__ = 'block'

    id = db.Column(db.Integer, primary_key=True)
    id_station = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)
    name = db.Column(db.String(300))
    order = db.Column(db.Integer, nullable=False)

    questions = db.relationship('Question', backref='block')
