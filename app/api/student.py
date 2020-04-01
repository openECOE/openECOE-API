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
from flask_potion.routes import Relation, ItemRoute

from app.model.Student import Answer, Student
from app.api.ecoe import EcoeChildResource
from app.api._mainresource import OpenECOEResource


class AnswerResource(OpenECOEResource):

    class Meta:
        name = 'answers'
        model = Answer

        permissions = {
            'read': 'read:question',
            'create': 'manage',
            'update': 'manage',
            'delete': 'manage',
            'manage': 'manage:question'
        }

    class Schema:
        question = fields.ToOne('questions')
        student = fields.ToOne('students')


class StudentResource(EcoeChildResource):
    answers = Relation('answers')

    class Meta:
        name = 'students'
        model = Student

    class Schema:
        ecoe = fields.ToOne('ecoes')
        planner = fields.ToOne('planners', nullable=True)

    @ItemRoute.GET('/answers/all')
    def get_all_answers(self, student) -> fields.List(fields.Inline(AnswerResource)):
        return student.answers.all()


@signals.before_update.connect_via(StudentResource)
def before_update_planner(sender, item, changes):
    if 'planner' in changes.keys():
        # Reorder students from old planner
        if item.planner and item.planner_order:
            # If the item has another planner reorder the old planner students
            old_planner_students = Student.query \
                .filter(Student.id_planner == item.planner.id) \
                .filter(Student.id != item.id) \
                .filter(Student.planner_order > item.planner_order) \
                .order_by(Student.planner_order).all()

            for order, student in enumerate(old_planner_students):
                student.planner_order = order + item.planner_order
