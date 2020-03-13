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

from flask_potion import fields
from flask_potion.routes import Relation
from app.model.Question import Block, Question
from .user import PrincipalResource

station_permissions = {
            'read': 'read:station',
            'create': 'manage',
            'update': 'manage',
            'delete': 'manage',
            'manage': 'manage:station'
        }


class QuestionResource(PrincipalResource):
    answers = Relation('answers')

    class Meta:
        name = 'questions'
        model = Question

        permissions = station_permissions

    class Schema:
        area = fields.ToOne('areas')
        station = fields.ToOne('stations')
        block = fields.ToOne('blocks')


class BlockResource(PrincipalResource):
    questions = Relation('questions')

    class Meta:
        name = 'blocks'
        model = Block

        permissions = station_permissions

    class Schema:
        station = fields.ToOne('stations')
