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
from app.model.Question import Block
from sqlalchemy.exc import SQLAlchemyError

class Station(db.Model):
    __tablename__ = 'station'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    id_ecoe = db.Column(db.Integer, db.ForeignKey('ecoe.id'), nullable=False)
    order = db.Column(db.Integer)
    id_parent_station = db.Column(db.Integer, db.ForeignKey('station.id'))

    id_manager = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    schedules = db.relationship('Schedule', backref='station')
    blocks = db.relationship('Block', backref='station')
    questions = db.relationship('Question', backref='station')
    answers = db.relationship('Answer', backref='station')

    # adjacency list pattern
    children_stations = db.relationship('Station', backref=db.backref('parent_station', remote_side=[id]))

    __table_args__ = (
        db.UniqueConstraint(name, id_ecoe, name='station_ecoe_uk'),
        db.Index('ix_station_parent', id_parent_station)
    )

    # @ItemRoute.GET('/student/<int:student>/answers')
    # def get_student_answers:
    
    def export(self):
        station_json = {
            "name": self.name,
            "order": self.order,
            "blocks": [block.export() for block in self.blocks],
            "children": [child.export() for child in self.children_stations]
        }
        return station_json

    def clone_blocks(self, blocks: list[Block]):
        try:
            for original_block in blocks:
                clonned_block = Block(id_station = self.id, name = original_block.name, 
                                    order = original_block.order)
                db.session.add(clonned_block)
                clonned_block.clone_questions(original_block.questions)

            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise
        except Exception:
            db.session.rollback()
            raise