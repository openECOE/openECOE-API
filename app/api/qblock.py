from flask_potion import fields, signals
from flask_potion.routes import Relation
from .user import PrincipalResource


from app.model.QBlock import QBlock


class QblockResource(PrincipalResource):
    questions = Relation('questions')

    class Meta:
        name = 'qblocks'
        model = QBlock

        permissions = {
            'read': 'read:station',
            'create': 'manage',
            'update': 'manage',
            'delete': 'manage',
            'manage': 'manage:station'
        }

    class Schema:
        station = fields.ToOne('stations')


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

# TODO: Review Creation QBlock order
# @signals.before_create.connect_via(QblockResource)
# def before_create_qblock(sender, item):
#     order_qblock(item)

@signals.before_delete.connect_via(QblockResource)
def before_delete_qblock(sender, item):
    order_qblock(item, 'del')