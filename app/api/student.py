from flask_potion import ModelResource, fields, signals
from flask_potion.routes import Relation, ItemRoute, RouteSet, ResourceBound, ResourceReference, cached_property, RelationInstances, attribute_to_route_uri, to_camel_case
from app.model.Student import Student
from app.model.Question import QType

from flask_potion.reference import _bind_schema
from flask_potion.fields import ToOne, Integer
from flask_potion.fields import _field_from_object
from flask_potion.instances import Instances, RelationInstances
from flask_potion.reference import ResourceBound, ResourceReference
from flask_potion.schema import Schema, FieldSet
from flask_potion.utils import get_value


class RelationSpecial(RouteSet, ResourceBound):
    """
    Used to define a relation to another :class:`ModelResource`.
    """

    def __init__(self, resource, backref=None, io="rw", attribute=None, **kwargs):
        self.reference = ResourceReference(resource)
        self.attribute = attribute
        self.backref = backref
        self.io = io

    @cached_property
    def target(self):
        return self.reference.resolve(self.resource)

    # FIXME can only be loaded after target is added to API
    def routes(self):
        io = self.io
        rule = '/{}'.format(attribute_to_route_uri(self.attribute))

        relation_route = ItemRoute(rule=rule)
        relations_route = ItemRoute(rule=rule)

        if "r" in io:
            def relation_instances(resource, item, page, per_page):
                return resource.manager.relation_instances(item,
                                                           self.attribute,
                                                           self.target,
                                                           page,
                                                           per_page)

            yield relations_route.for_method('GET',
                                             relation_instances,
                                             rel=self.attribute,
                                             response_schema=RelationInstances(self.target),
                                             schema=FieldSet({
                                                 "page": Integer(minimum=1, default=1),
                                                 "per_page": Integer(minimum=1,
                                                                     default=20,  # FIXME use API reference
                                                                     maximum=50)
                                             }))

        if "w" in io or "u" in io:
            def relation_add(resource, item, target_item):
                resource.manager.relation_add(item, self.attribute, self.target, target_item)
                resource.manager.commit()
                return target_item

            yield relations_route.for_method('POST',
                                             relation_add,
                                             rel=to_camel_case('add_{}'.format(self.attribute)),
                                             response_schema=ToOne(self.target),
                                             schema=ToOne(self.target))

            def relation_remove(resource, item, target_item):
                resource.manager.relation_remove(item, self.attribute, self.target, target_item)
                resource.manager.commit()
                return None, 204

            yield relation_route.for_method('DELETE',
                                            relation_remove,
                                            rel=to_camel_case('remove_{}'.format(self.attribute)),
                                            response_schema=ToOne(self.target),
                                            schema=ToOne(self.target))


class StudentResource(ModelResource):
    answers = RelationSpecial('option')

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
        if item.planner:
            old_planner_students = Student.query\
                .filter(Student.id_planner == item.planner.id)\
                .filter(Student.id != item.id)\
                .filter(Student.planner_order > item.planner_order)\
                .order_by(Student.planner_order).all()

            for order, student in enumerate(old_planner_students):
                student.planner_order = order + item.planner_order

        item.planner_order = len(changes['planner'].students) + 1

@signals.before_add_to_relation.connect_via(StudentResource)
def before_add_relation(sender, item, attribute, child):
    if attribute == 'answers':
        if child.question.question_type == QType.RADIO_BUTTON:
            # Delete other answers for this question
            answers_question = filter(lambda answer_q: answer_q.id_question == child.question.id, item.answers)
            for answer in answers_question:
                sender.manager.relation_remove(item, attribute, StudentResource, answer)

