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

from app.model import db
from sqlalchemy.dialects import mysql


class Student(db.Model):
    __tablename__ = 'student'


    id = db.Column(db.Integer, primary_key=True)
    id_ecoe = db.Column(db.Integer, db.ForeignKey('ecoe.id'), nullable=False)
    id_planner = db.Column(db.Integer, db.ForeignKey('planner.id'), nullable=True)
    name = db.Column(db.String(50), nullable=False)
    surnames = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(10))  # dni is not unique

    planner_order = db.Column(db.Integer)

    answers = db.relationship('Answer', backref='student')

    __table_args__ = (
        db.UniqueConstraint(name, surnames, id_ecoe, name='student_name_ecoe_uk'),
    )


class Answer(db.Model):
    __tablename__ = 'answer'

    id = db.Column(db.Integer, primary_key=True)
    id_station = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)
    id_student = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    id_question = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    answer_schema = db.Column(mysql.LONGTEXT())
    points = db.Column(db.Numeric(10, 2))

    __table_args__ = (
        db.UniqueConstraint(id_station, id_student, id_question, name='answer_student_question_uk'),
    )