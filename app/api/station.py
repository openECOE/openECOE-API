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
from app.api.user import PermissionResource, UserResource
from app.model.Station import Station
from app.model.Question import Question, Block
from app.model.User import PermissionType, RoleType
from .ecoe import EcoeChildResource
from flask_potion.exceptions import BadRequest

class StationResource(EcoeChildResource):
    schedules = Relation('schedules')
    blocks = Relation('blocks')
    questions = Relation('questions')
    answers = Relation('answers')

    class Meta:
        name = 'stations'
        model = Station
        natural_key = ('ecoe', 'name')
        write_only_fields = ['user']
        
        permissions = {
            'read': ['manage', 'evaluate', 'read:ecoe'],
            'create': 'manage',
            'update': 'manage',
            'delete': 'manage',
            'manage': [PermissionType.MANAGE + ':ecoe', PermissionType.MANAGE, RoleType.ADMIN],
            'evaluate': [PermissionType.EVALUATE + ':ecoe', PermissionType.EVALUATE, 'manage']
        }
        

    class Schema:
        ecoe = fields.ToOne('ecoes')
        user = fields.ToOne('users', nullable=True)
        parent_station = fields.ToOne('stations', nullable=True)
        children_stations = fields.ToMany('stations', nullable=True)


def check_child_stations_order(station, order):
    if(len(station.children_stations) > 0):
        for child_station in station.children_stations:
            if order >= child_station.order:
                    return False
    
    return True

def check_parent_stations_order(station, order):
    if station.parent_station is None:
        return True
    return order > station.parent_station.order 

def order_station(item, new_order, operation='add'):
    stations_ecoe = len(item.ecoe.stations)
    if item.order > stations_ecoe or item.order < 1:
        item.order = stations_ecoe
    else:
        stations_ecoe = Station.query.filter(Station.id_ecoe == item.ecoe.id).order_by(Station.order).all()
        station_idx = item.order - 1
        if operation == 'add': 
            stations_ecoe.insert(new_order - 1, stations_ecoe.pop(station_idx))
        else: # operation is delete
            stations_ecoe.pop(station_idx)

        for idx, station in enumerate(stations_ecoe):
            station.order = idx + 1

@signals.before_update.connect_via(StationResource)
def before_update_station(sender, item, changes):
    if 'order' in changes.keys():
        if not check_child_stations_order(item, changes['order']) or \
            not check_parent_stations_order(item, changes['order']):
            raise BadRequest(description="Orden de estacion no valido")

        order_station(item, changes['order'])


# TODO: Review Create Station Order
# Add permissions to manage to creator
@signals.before_create.connect_via(StationResource)
def before_create_station(sender, item):
    # order_station(item)
    if not item.user:
        item.user = current_user


@signals.before_delete.connect_via(StationResource)
def before_delete_station(sender, item):
    Question.query.filter(Question.id_station == item.id).delete()
    Block.query.filter(Block.id_station == item.id).delete()

    if len(item.ecoe.stations) > 1:
        order_station(item, item.order, 'del')
    
    
@signals.before_create.connect_via(PermissionResource)
def on_before_create_permission(sender, item):
    if item.name == 'evaluate' and item.object == 'stations':
        station = StationResource.manager.read(item.id_object)
        has_read_permission = False
        for permission in item.user.permissions:
            if permission.id_object is station.id_ecoe and permission.name == 'read' and permission.object == 'ecoes':
                has_read_permission = True
        
        if not has_read_permission:
            sender.manager.create({
                'user': item.user,
                'id_object': station.id_ecoe,
                'name': 'read',
                'object': 'ecoes'})

