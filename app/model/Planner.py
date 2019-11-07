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


class Planner(db.Model):
    __tablename__ = 'planner'

    id = db.Column(db.Integer, primary_key=True)
    id_shift = db.Column(db.Integer, db.ForeignKey('shift.id'), nullable=False)
    id_round = db.Column(db.Integer, db.ForeignKey('round.id'), nullable=False)

    students = db.relationship('Student', backref='planner')

    __table_args__ = (
        db.UniqueConstraint(id_shift, id_round, name='shift_round_uk'),
    )