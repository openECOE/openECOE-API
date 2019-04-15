from flask_potion import ModelResource, fields, signals
from flask_potion.routes import Relation
from app.model.Student import Student
from app.model.Question import QType


class StudentResource(ModelResource):
    answers = Relation('option')

    class Meta:
        model = Student
        natural_key = ('name', 'surnames')

    class Schema:
        ecoe = fields.ToOne('ecoe')
        planner = fields.ToOne('planner', nullable=True)
        answers = fields.ToMany('option')


@signals.before_create.connect_via(StudentResource)
def before_add_planner(sender, item):
    if item.planner:
        item.planner_order = len(item.planner.students)


@signals.before_update.connect_via(StudentResource)
def before_update_planner(sender, item, changes):
    if 'planner' in changes.keys():
        # Reorder students from old planner
        if changes['planner']:
            planner_order = 0

            if item.planner_order:
                planner_order = item.planner_order

            # If the item has another planner reorder the old planner students
            if item.planner:
                old_planner_students = Student.query \
                    .filter(Student.id_planner == item.planner.id) \
                    .filter(Student.id != item.id) \
                    .filter(Student.planner_order > planner_order) \
                    .order_by(Student.planner_order).all()

                for order, student in enumerate(old_planner_students):
                    student.planner_order = order + planner_order

            item.planner_order = len(changes['planner'].students) + 1


@signals.before_add_to_relation.connect_via(StudentResource)
def before_add_relation(sender, item, attribute, child):
    if attribute == 'answers':
        if child.question.question_type in [QType.RADIO_BUTTON, QType.RANGE_SELECT]:
            # Delete other answers for this question
            answers_question = filter(lambda answer_q: answer_q.id_question == child.question.id, item.answers)
            for answer in answers_question:
                sender.manager.relation_remove(item, attribute, StudentResource, answer)
