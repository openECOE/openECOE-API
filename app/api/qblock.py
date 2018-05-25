from flask_potion import ModelResource, fields, signals
from flask_potion.routes import Relation, ItemRoute, RouteSet, ResourceBound, ResourceReference, cached_property, RelationInstances, attribute_to_route_uri, to_camel_case
from flask_potion.reference import _bind_schema
from flask_potion.fields import ToOne, Integer
from flask_potion.fields import _field_from_object
from flask_potion.instances import Instances, RelationInstances
from flask_potion.reference import ResourceBound, ResourceReference
from flask_potion.schema import Schema, FieldSet
from flask_potion.utils import get_value

from app.model.QBlock import QBlock

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


class QblockResource(ModelResource):
    questions = RelationSpecial('question')

    class Meta:
        model = QBlock

    class Schema:
        station = fields.ToOne('station')
        questions = fields.ToMany('question')


def order_qblock(item, op='add'):
    order_correction = 0

    qblocks_station = len(item.station.qblocks)
    if not item.order or item.order > qblocks_station or item.order < 1:
        item.order = qblocks_station
    else:
        qblocks_station = QBlock.query \
            .filter(QBlock.id_station == item.station.id).filter(QBlock.order >= item.order) \
            .filter(QBlock.id != item.id).order_by(QBlock.order).all()

        if op == 'add':
            order_correction = 1

        for order, qblock_station in enumerate(qblocks_station):
            qblock_station.order = order + item.order + order_correction


@signals.before_update.connect_via(QblockResource)
def before_update_qblock(sender, item, changes):
    if 'order' in changes.keys():
        item.order = changes['order']
        order_qblock(item)

@signals.before_create.connect_via(QblockResource)
def before_create_qblock(sender, item):
    order_qblock(item)

@signals.before_delete.connect_via(QblockResource)
def before_delete_qblock(sender, item):
    order_qblock(item, 'del')