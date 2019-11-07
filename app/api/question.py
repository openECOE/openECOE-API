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
from flask_potion.routes import Relation, ItemRoute
from app.model.Question import Question, QType
from .user import PrincipalResource


class QuestionResource(PrincipalResource):
    options = Relation('options')

    @ItemRoute.GET('/points')
    def points(self, question) -> fields.Integer():
        return question.points

    class Meta:
        name = 'questions'
        model = Question

        permissions = {
            'read': 'read:area',
            'create': 'managCe',
            'update': 'manage',
            'delete': 'manage',
            'manage': 'manage:area'
        }

    class Schema:
        area = fields.ToOne('areas')
        question_type = fields.String(enum=QType)
        options = fields.ToMany('options')
        qblocks = fields.ToMany('qblocks')

# TODO: Comprobar al crear una pregunta que el area y el grupo introducido pertenecen a la misma ECOE
