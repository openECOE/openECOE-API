from flask_potion import ModelResource, fields, signals
from flask_potion.routes import Relation
from app.model.Student import Student


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
@signals.before_update.connect_via(StudentResource)
def before_add_planner(sender, item, changes={}):
    if 'planner' in changes.keys():
        # Reorder students from old planner
        old_planner_students = Student.query\
            .filter(Student.id_planner == item.planner.id)\
            .filter(Student.id != item.id)\
            .filter(Student.planner_order > item.planner_order)\
            .order_by(Student.planner_order).all()

        for order, student in enumerate(old_planner_students):
            student.planner_order = order + item.planner_order

        item.planner_order = len(changes['planner'].students) + 1
    else:
        if item.planner:
            item.planner_order = len(item.planner.students)
