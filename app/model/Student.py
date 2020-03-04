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
from app.model.many_to_many_tables import students_options


class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surnames = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(10))  # dni is not unique

    id_ecoe = db.Column(db.Integer, db.ForeignKey('ecoe.id'), nullable=False)
    id_planner = db.Column(db.Integer, db.ForeignKey('planner.id'), nullable=True)
    planner_order = db.Column(db.Integer)

    answers = db.relationship('Option', secondary=students_options, lazy='dynamic', back_populates='students')

    __table_args__ = (
        db.UniqueConstraint(name, surnames, id_ecoe, name='student_name_ecoe_uk'),
    )


class Answer(db.Model):
    __tablename__ = 'answer'

    id = db.Column(db.Integer, primary_key=True)
    id_student = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    id_question = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    answer = db.Column(db.JSON)
    points = db.Column(db.Integer)

    __table_args__ = (
        db.UniqueConstraint(id_student, id_question, name='answer_student_question_uk'),
    )