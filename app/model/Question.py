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
from app.model.Area import Area
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify
from flask import json

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

    def export(self) -> str:
        # TODO: ver lo del _ en options

        area = Area.query.get(self.id_area)
        question_json = json.loads(self.question_schema)
        question_json['area'] = {
            "name": area.name,
            "code": area.code
        }

        return question_json


class Block(db.Model):
    __tablename__ = 'block'

    id = db.Column(db.Integer, primary_key=True)
    id_station = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)
    name = db.Column(db.String(300))
    order = db.Column(db.Integer, nullable=False)

    questions = db.relationship('Question', backref='block')

    def export(self) -> str:
        block_json = {
            "name": self.name,
            "order": self.order,
            "questions": [question.export() for question in self.questions]
        }

        return block_json

    def get_or_create_area(self, id_ecoe: int, original_area: Area) -> Area:
        # If the area of the question exists in the 
        # ecoe use that, else create a new one with the same name
        area = Area.query.filter(
            (Area.id_ecoe == id_ecoe) & 
            ((Area.name == original_area.name) | (Area.code == original_area.code))
        ).first()
        
        if area is None:
            area = Area(name = original_area.name, id_ecoe = id_ecoe, code = original_area.code)
            db.session.add(area)
            db.session.flush()
        
        return area

    def clone_questions(self, questions: list[Question]):
        from app.model.Station import Station
        id_ecoe = Station.query.get(self.id_station).id_ecoe
        
        try:
            for original_question in questions:
                original_area = Area.query.get(original_question.id_area)
                area = self.get_or_create_area(id_ecoe, original_area)

                clonned_question = Question(id_area = area.id, order = original_question.order,
                                        id_block = self.id, id_station = self.id_station,
                                        question_schema = original_question.question_schema, 
                                        max_points = original_question.max_points)
            
                db.session.add(clonned_question)

            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise
        except Exception:
            db.session.rollback()
            raise
