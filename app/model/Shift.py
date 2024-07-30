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


class Shift(db.Model):
    __tablename__ = 'shift'

    id = db.Column(db.Integer, primary_key=True)
    id_ecoe = db.Column(db.Integer, db.ForeignKey('ecoe.id'))
    shift_code = db.Column(db.String(20), nullable=False)
    time_start = db.Column(db.DateTime(), nullable=False)

    planners = db.relationship('Planner', backref='shift')

    __table_args__ = (
        db.UniqueConstraint(shift_code, id_ecoe, name='shift_ecoe_uk'),
    )

    def export(self) -> dict:
        shift_json = {
            "shift_code": self.shift_code,
            "time_start": self.time_start
        }

        return shift_json