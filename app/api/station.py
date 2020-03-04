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

from flask_login import current_user
from flask_potion import fields, signals
from flask_potion.routes import Relation
from app.model.Station import Station
from .ecoe import EcoePrincipalResource


class StationResource(EcoePrincipalResource):
    schedules = Relation('schedules')
    blocks = Relation('blocks')
    questions = Relation('questions')

    class Meta:
        name = 'stations'
        model = Station
        natural_key = ('ecoe', 'name')

        permissions = {
            'read': 'manage',
            'create': 'manage',
            'update': 'manage',
            'delete': 'manage',
            'manage': ['manage:ecoe', 'manage', 'user:user']
        }

    class Schema:
        ecoe = fields.ToOne('ecoes')
        user = fields.ToOne('users', nullable=True)
        parent_station = fields.ToOne('stations', nullable=True)
        children_stations = fields.ToMany('stations', nullable=True)


def order_station(item, op='add'):
    order_correction = 0

    stations_ecoe = len(item.ecoe.stations)
    if not item.order or item.order > stations_ecoe or item.order < 1:
        item.order = stations_ecoe
    else:
        stations_ecoe = Station.query \
            .filter(Station.id_ecoe == item.ecoe.id).filter(Station.order >= item.order) \
            .filter(Station.id != item.id).order_by(Station.order).all()

        if op == 'add':
            order_correction = 1

        for order, station_ecoe in enumerate(stations_ecoe):
            station_ecoe.order = order + item.order + order_correction


@signals.before_update.connect_via(StationResource)
def before_update_station(sender, item, changes):
    if 'order' in changes.keys():
        item.order = changes['order']
        order_station(item)


# TODO: Review Create Station Order
# Add permissions to manage to creator
@signals.before_create.connect_via(StationResource)
def before_create_station(sender, item):
    # order_station(item)
    if not item.user:
        item.user = current_user


@signals.before_delete.connect_via(StationResource)
def before_delete_station(sender, item):
    order_station(item, 'del')
