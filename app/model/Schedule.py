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
from app.model.Station import Station
from app.model.Event import Event

class Schedule(db.Model):
    __tablename__ = 'schedule'

    id = db.Column(db.Integer, primary_key=True)
    id_ecoe = db.Column(db.Integer, db.ForeignKey('ecoe.id'))
    id_stage = db.Column(db.Integer, db.ForeignKey('stage.id'), nullable=False)
    id_station = db.Column(db.Integer, db.ForeignKey('station.id'))

    events = db.relationship('Event', backref='schedule')

    __table_args__ = (
        db.UniqueConstraint(id_ecoe, id_stage, id_station, name='ecoe_stage_station_uk'),
    )

    def import_event(self, event):
        try:
            imported_event = Event(id_schedule = self.id, time = event["time"], sound = event["sound"], text = event["text"])
            db.session.add(imported_event)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    def export(self) -> dict:
        station_order = None
        if self.id_station is not None:
            station_order = Station.query.get(self.id_station).order

        schedule_json = {
            "events": [event.export() for event in self.events],
            "station": station_order
        }
        return schedule_json