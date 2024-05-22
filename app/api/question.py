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

from flask_potion import fields, signals
from flask_potion.routes import Relation
from app.model.Question import Block, Question
from app.api._mainresource import OpenECOEResource
from app.shared import order_items, calculate_order

station_permissions = {
            'read': 'read:station',
            'create': 'manage',
            'update': 'manage',
            'delete': 'manage',
            'manage': 'manage:station'
        }


class QuestionResource(OpenECOEResource):
    answers = Relation('answers')

    class Meta:
        name = 'questions'
        model = Question

        permissions = station_permissions

    class Schema:
        area = fields.ToOne('areas')
        station = fields.ToOne('stations')
        block = fields.ToOne('blocks')


class BlockResource(OpenECOEResource):
    questions = Relation('questions')

    class Meta:
        name = 'blocks'
        model = Block

        permissions = station_permissions

    class Schema:
        station = fields.ToOne('stations')

def recalculate_question_order(id_station):
    blocks = Block.query.filter(Block.id_station == id_station).order_by(Block.order).all()
    unordered_questions = []
    for block in blocks:
        questions_by_block = [question for question in Question.query.filter(Question.id_block == block.id).order_by(Question.order).all()]
        unordered_questions.extend()

    calculate_order(unordered_questions)

@signals.before_update.connect_via(BlockResource)
def before_update_block(sender, item, changes):
    if 'order' in changes.keys():
        blocks = Block.query.filter(Block.id_station == item.id_station).order_by(Block.order).all()
        order_items(item, blocks, changes['order'], 'add')
        recalculate_question_order(item.id_station)

@signals.before_delete.connect_via(BlockResource)
def before_delete_block(sender, item):
    try:
        db.session.query(Question).filter(Question.id_block == item.id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    blocks = Block.query.filter(Block.id_station == item.id_station).order_by(Block.order).all()

    if len(blocks) > 1:
        order_items(item, blocks, item.order, 'del')
        recalculate_question_order(item.id_station)

@signals.before_update.connect_via(QuestionResource)
def before_update_question(sender, item, changes):
    if 'order' in changes.keys():
        questions = Question.query.filter(Question.id_station == item.id_station).order_by(Question.order).all()
        order_items(item, questions, changes['order'], 'add')

@signals.before_delete.connect_via(QuestionResource)
def before_delete_question(sender, item):
    questions = Question.query.filter(Question.id_station == item.id_station).order_by(Question.order).all()
    if len(questions) > 1:
        order_items(item, questions, item.order, 'del')