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
from app.api.question import BlockResource
from app.model.Station import Station
from app.model.Question import Question, Block
from app.model.User import PermissionType, RoleType
from .ecoe import EcoeChildResource
from flask_potion.exceptions import BadRequest
from flask_potion.exceptions import Conflict
from app.shared import order_items, calculate_order
from werkzeug.exceptions import Forbidden
from app.model import db

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

@signals.before_update.connect_via(StationResource)
def before_update_station(sender, item, changes):
    if 'name' in changes.keys():
        stations = Station.query.filter(Station.id_ecoe == item.ecoe.id).order_by(Station.order).all()
        for station in stations:
            if changes['name'] == station.name:
                raise BadRequest(description="El nombre de la estación ya existe")
    if 'order' in changes.keys():
        if not check_child_stations_order(item, changes['order']) or \
            not check_parent_stations_order(item, changes['order']):
            raise BadRequest(description="El orden de la estación padre debe ser menor que la de la subestación")

        stations = Station.query.filter(Station.id_ecoe == item.ecoe.id).order_by(Station.order).all()
        order_items(item, stations, changes['order'], 'add')


# TODO: Review Create Station Order
# Add permissions to manage to creator
@signals.before_create.connect_via(StationResource)
def before_create_station(sender, item):
    # order_station(item)
    if not item.user:
        item.user = current_user

@signals.after_create.connect_via(StationResource)
def after_create_station(sender, item):
    stations = Station.query.filter(Station.id_ecoe == item.ecoe.id).order_by(Station.id).all()
    if len(stations) > 1:
        calculate_order(stations)
        for station in stations: db.session.add(station)
        db.session.commit()       

@signals.before_delete.connect_via(StationResource)
def before_delete_station(sender, item):
    # Si tiene estaciones hijo no se puede borrar
    stations = Station.query.filter(Station.id_ecoe == item.ecoe.id).order_by(Station.order).all()
    for station in stations:
        if station.id_parent_station == item.id:
            raise Forbidden(description="No se ha podido borrar la estación debido a que es padre de otras estaciones")

    blocks = Block.query.filter(Block.id_station == item.id).all()
    for block in blocks:
        BlockResource.manager.delete_by_id(block.id)

@signals.after_delete.connect_via(StationResource)
def after_delete_station(sender, item):
    stations = Station.query.filter(Station.id_ecoe == item.id_ecoe).order_by(Station.order).all()
    if len(stations) > 1:
        calculate_order(stations)
        for station in stations: db.session.add(station)
        db.session.commit()
    
    
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

