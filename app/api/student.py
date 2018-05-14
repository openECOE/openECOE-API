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
        item.planner_order = len(changes['planner'].students) + 1
        # TODO: Reorder students from old planner
    else:
        if item.planner:
            item.planner_order = len(item.planner.students)
