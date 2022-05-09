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
from flask_potion.exceptions import ItemNotFound
from flask_potion.routes import Relation, ItemRoute
from sqlalchemy.orm import Session

from app.model.Student import Student
from app.model.Question import QType
from app.api.ecoe import EcoePrincipalResource
from app.api.option import OptionResource
from app.model.many_to_many_tables import students_options

from app import db


class StudentResource(EcoePrincipalResource):
    answers = Relation('options')

    class Meta:
        name = 'students'
        model = Student
        natural_key = ('name', 'surnames')

    class Schema:
        ecoe = fields.ToOne('ecoes')
        planner = fields.ToOne('planners', nullable=True)

    # @ItemRoute.GET('/answers/all')
    # def get_option(self) -> fields.Inline(OptionResource):
    #
    #
    #     return item
    #     # if item in student.answers:
    #     #     return item
    #     # else:
    #     #     raise ItemNotFound(OptionResource, id=option)

    @ItemRoute.GET('/answers/<int:option_id>')
    def get_option(self, student, option_id) -> fields.Inline(OptionResource):
        # item = OptionResource.manager.read(option)
        item = student.answers.filter_by(id = option_id).first()

        # return item
        if item is None:
            raise ItemNotFound(OptionResource, id=option_id)
        else:        
            return item
        
    @ItemRoute.DELETE('/answers/<int:option_id>')
    def del_option(self, student, option_id) -> fields.Inline(OptionResource):
        item = student.answers.filter_by(id = option_id).first()
        
        if item is None:
            raise ItemNotFound(OptionResource, id=option_id)
        else:
            student.answers.remove(item)
            db.session.commit()
            return None, 204
            
        

    @ItemRoute.GET('/answers/all')
    def get_all_answers(self, student) -> fields.List(fields.Inline(OptionResource)):
        return student.answers.all()

    # @ItemRoute.GET('/answers/station/<int:station_id>')
    # def find_answer(self, student, option_id) -> fields.Inline(OptionResource):
    #
    #     student_option = db.session.query(students_options) \
    #         .filter(students_options.c.student_id == student.id) \
    #         .filter(students_options.c.option_id == option_id).first()
    #
    #     return OptionResource.manager.read(student_option.option_id)

# @signals.before_create.connect_via(StudentResource)
# def before_add_planner(sender, item):
#     if item.planner:
#         item.planner_order = len(item.planner.students)


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


@signals.before_add_to_relation.connect_via(StudentResource)
def before_add_relation(sender, item, attribute, child):
    if attribute == 'answers':
        if child.question.question_type in [QType.RADIO_BUTTON, QType.RANGE_SELECT]:
            # Delete other answers for this question
            answers_question = filter(lambda answer_q: answer_q.id_question == child.question.id, item.answers)
            for answer in answers_question:
                sender.manager.relation_remove(item, attribute, StudentResource, answer)
