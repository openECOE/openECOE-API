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


class Round(db.Model):
    __tablename__ = 'round'

    id = db.Column(db.Integer, primary_key=True)
    id_ecoe = db.Column(db.Integer, db.ForeignKey('ecoe.id'))
    round_code = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

    planners = db.relationship('Planner', backref='round')

    __table_args__ = (
        db.UniqueConstraint(round_code, id_ecoe, name='round_ecoe_uk'),
    )

    def export(self) -> dict:
        round_json = {
            "round_code": self.round_code,
            "description": self.description
        }

        return round_json