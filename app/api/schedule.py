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

from flask_potion import fields
from flask_potion.routes import Relation
from app.model.Schedule import Schedule
from app.api.ecoe import EcoeChildResource


class ScheduleResource(EcoeChildResource):
    events = Relation('events')

    class Meta:
        name = 'schedules'
        model = Schedule

    class Schema:
        ecoe = fields.ToOne('ecoes', nullable=True)
        stage = fields.ToOne('stages')
        station = fields.ToOne('stations', nullable=True)


