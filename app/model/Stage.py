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

from app.model import db
from app.model.Schedule import Schedule
from app.model.Station import Station

class Stage(db.Model):
    __tablename__ = 'stage'

    id = db.Column(db.Integer, primary_key=True)
    id_ecoe = db.Column(db.Integer, db.ForeignKey('ecoe.id'), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # in seconds
    order = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)

    schedules = db.relationship('Schedule', backref='stage')

    def import_schedule(self, schedule):
        station_id = None
        if schedule['station'] is not None:
            station_id = Station.query \
                .filter(Station.id_ecoe == self.id_ecoe) \
                .filter(Station.order == schedule['station']).first().id

        try:
            imported_schedule = Schedule(id_ecoe = self.id_ecoe, id_stage = self.id, id_station = station_id)
            db.session.add(imported_schedule)
            db.session.flush()
            
            for event in schedule["events"]:
                imported_schedule.import_event(event)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    def export(self) -> dict:
        stage_json = {
            "duration": self.duration,
            "name": self.name,
            "order": self.order,
            "schedules": [schedule.export() for schedule in self.schedules]
        }

        return stage_json
