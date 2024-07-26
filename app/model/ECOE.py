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
import base64
import os
from enum import Enum

import requests
from flask import current_app
from flask_login import current_user
from flask_potion.exceptions import BackendConflict, PageNotFound
from sqlalchemy.dialects import mysql
from sqlalchemy.exc import SQLAlchemyError
from app.model import db
from app.model.Station import Station
from app.shared import calculate_order

class ChronoNotFound(PageNotFound):
    def __init__(self, **kwargs):
        self.data = kwargs
        self.data.update(description="Chrono module not found")

    def as_dict(self):
        dct = super(PageNotFound, self).as_dict()
        dct.update(self.data)
        return dct


class ECOEstatus(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"


class ECOE(db.Model):
    __tablename__ = "ecoe"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    id_organization = db.Column(
        db.Integer, db.ForeignKey("organization.id"), nullable=False
    )

    id_coordinator = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    status = db.Column(db.Enum(ECOEstatus), nullable=False, default=ECOEstatus.DRAFT)
    chrono_token = db.Column(db.String(250), nullable=True)
    description = db.Column(mysql.LONGTEXT())
    id_job_reports = db.Column(db.String(36), db.ForeignKey('job.id'), nullable=True)
    id_job_csv = db.Column(db.String(36), db.ForeignKey('job.id'), nullable=True)

    areas = db.relationship("Area", backref="ecoe")
    stations = db.relationship("Station", backref="ecoe")
    schedules = db.relationship("Schedule", backref="ecoe")
    students = db.relationship("Student", backref="ecoe")
    rounds = db.relationship("Round", backref="ecoe")
    shifts = db.relationship("Shift", backref="ecoe", order_by="Shift.time_start")
    stages = db.relationship("Stage", backref="ecoe")
    report_templates = db.relationship("ReportTemplate", backref="ecoe")
    job_reports = db.relationship("Job", foreign_keys=[id_job_reports])
    job_csv = db.relationship("Job",foreign_keys=[id_job_csv])

    @property
    def configuration(self):

        stages = []
        stage_events = {}

        for sch in self.schedules:
            if sch.stage not in stages:
                stages.append(sch.stage)
                stage_events.update({sch.stage.id: []})

            for ev in sch.events:
                stage_events[sch.stage.id].append(
                    {
                        "t": ev.time,
                        "message": ev.text,
                        "sound": ev.sound,
                        "stations": [0] + [station.id for station in self.stations]
                        if sch.station is None
                        else [sch.station.id],
                        "is_countdown": ev.is_countdown,
                    }
                )

        exists_dependant = False

        for station in self.stations:
            if station.parent_station is not None:
                exists_dependant = True
                break

        time_start = ""

        try:
            time_start = self.shifts[0].time_start
        except IndexError:
            pass

        config = {
            "ecoe": {
                "id": self.id,
                "name": self.name,
                "organization": self.id_organization,
                "time_start": time_start.__str__() + " GMT+0000",
            },
            "rounds": [{"id": r.id, "name": r.description} for r in self.rounds],
            "rounds_id": [r.id for r in self.rounds],
            "reruns": len(self.stations) + (1 if exists_dependant else 0),
            "schedules": [
                {
                    "name": st.name,
                    "duration": st.duration,
                    "order": st.order,
                    "events": stage_events[st.id],
                }
                for st in stages
            ],
            "tfc": self.chrono_token,
        }

        return config

    def load_config(self):
        self.chrono_token = base64.b64encode(os.urandom(250)).decode("utf-8")[:250]
        db.session.commit()
        config = self.configuration
        endpoint = current_app.config["CHRONO_ROUTE"] + "/load"

        # sending post request and saving response as response object
        try:
            r = requests.post(url=endpoint, json=config)
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.ConnectTimeout,
        ):
            raise ChronoNotFound(url=endpoint)
        # extracting response text
        if r.status_code == 200:
            return self.configuration
        else:
            raise BackendConflict(
                err_chrono={
                    "url": r.url,
                    "status_code": r.status_code,
                    "reason": r.reason,
                    "text": r.text,
                    "config": config,
                }
            )

    def delete_config(self):
        endpoint = "%s/%d" % (current_app.config["CHRONO_ROUTE"], self.id)
        try:
            r = requests.delete(url=endpoint, headers={"tfc": self.chrono_token})
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.ConnectTimeout,
        ):
            raise ChronoNotFound(url=endpoint)
        # extracting response text
        if r.status_code == 200:
            self.chrono_token = None
        else:
            raise BackendConflict(
                err_chrono={
                    "url": r.url,
                    "status_code": r.status_code,
                    "reason": r.reason,
                    "text": r.text,
                }
            )

    def start(self):
        endpoint = "start/%d" % self.id
        return self.__call_chrono(endpoint)

    def play(self, round_id=None):
        endpoint = "play/%d" % self.id
        if round_id is not None:
            endpoint += "/" + str(round_id)
        return self.__call_chrono(endpoint)

    def pause(self, round_id=None):
        endpoint = "pause/%d" % self.id
        if round_id is not None:
            endpoint += "/" + str(round_id)
        return self.__call_chrono(endpoint)

    def abort(self):
        endpoint = "abort/%d" % self.id
        return self.__call_chrono(endpoint)

    def chrono_status(self):
        endpoint = "rounds-status/%d" % self.id
        chrono_route = current_app.config["CHRONO_ROUTE"]
        url = f"{chrono_route}/rounds-status/{self.id}"

        try:
            r = requests.get(url=url)
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.ConnectTimeout,
        ):
            raise ChronoNotFound(url=endpoint)

        if r.status_code != 200:
            raise BackendConflict(
                err_chrono={
                    "url": r.url,
                    "status_code": r.status_code,
                    "reason": r.reason,
                    "text": r.text,
                }
            )
        else:
            return r.json()

    def loop(self, loop):
        chrono_route = current_app.config["CHRONO_ROUTE"]
        url = f"{chrono_route}/loop/{self.id}"

        body = dict(loop=loop)     
        try:
            r = requests.post(url=url, headers={"tfc": self.chrono_token}, json=body)
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.ConnectTimeout,
        ):
            raise ChronoNotFound(url=url)
        
        if r.status_code != 200:
            raise BackendConflict(
                err_chrono={
                    "url": r.url,
                    "status_code": r.status_code,
                    "reason": r.reason,
                    "text": r.text,
                }
            )
        else:
            return {
                "url": r.url,
                "status_code": r.status_code,
                "reason": r.reason,
                "text": r.text,
            }
        
    def __call_chrono(self, endpoint):

        endpoint = "%s/%s" % (current_app.config["CHRONO_ROUTE"], endpoint)
        try:
            r = requests.post(url=endpoint, headers={"tfc": self.chrono_token})
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.ConnectTimeout,
        ):
            raise ChronoNotFound(url=endpoint)

        # extracting response text
        if r.status_code != 200:
            raise BackendConflict(
                err_chrono={
                    "url": r.url,
                    "status_code": r.status_code,
                    "reason": r.reason,
                    "text": r.text,
                }
            )
        else:
            return {
                "url": r.url,
                "status_code": r.status_code,
                "reason": r.reason,
                "text": r.text,
            }

    def reorder_created_stations(self):
        ecoe_stations = Station.query.filter(Station.id_ecoe == self.id).order_by(Station.id).all()
        if len(ecoe_stations) > 1:
            calculate_order(ecoe_stations)
            try:
                for station in ecoe_stations: 
                    db.session.add(station)

                db.session.commit()
            except SQLAlchemyError:
                raise

    def get_clonned_parent_station(self, original_station: Station) -> int:
        if original_station.id_parent_station is None:
            return None

        original_parent_station = Station.query.get(original_station.id_parent_station)

        clonned_parent_station = Station.query \
            .filter((Station.id_ecoe == self.id) & (Station.name == original_parent_station.name)) \
            .first()

        return clonned_parent_station.id if clonned_parent_station else None

    def get_clonned_station_name(self, original_station_name: str):
        stations = Station.query.filter(Station.id_ecoe == self.id).order_by(Station.id).all()
        suffix = "_copia"

        clonned_station_name = original_station_name
        while any(s.name == clonned_station_name for s in stations):
            clonned_station_name = clonned_station_name + suffix 
        
        return clonned_station_name

    def clone_stations(self, stations: list[Station]):
        stations.sort(key=lambda s: s.order, reverse=False)
        
        try:
            for original_station in stations:
                clonned_station_name = self.get_clonned_station_name(original_station.name)
                id_parent_station = self.get_clonned_parent_station(original_station)

                clonned_station = Station(name = clonned_station_name, 
                                        id_ecoe = self.id,
                                        order = original_station.order,
                                        id_parent_station = id_parent_station,
                                        id_manager=current_user.id)

                db.session.add(clonned_station)
                db.session.flush()
                clonned_station.clone_blocks(original_station.blocks)

            db.session.commit()
            self.reorder_created_stations()
               
        except SQLAlchemyError:
            db.session.rollback()
            raise
        except Exception:
            db.session.rollback()
            raise
    
    def import_station(self, station, id_parent_station):
        # Para importar las estaciones hijo lo que se va a hacer
        # es que las estaciones hijo no estarán al mismo nivel que 
        # el padre, siempre estarán dentro de la propiedad children
        # Ejemplo:
        # {
        #   "name": "Estación Padre",
        #   "order": 1,
        #   "blocks": [...],
        #   "children": [
        #       "name": "Estación Hija",
        #       "order": 2,
        #       "blocks": [...],
        #       "children": [ ]
        #   ],
        # }
        #
        # En este caso se está importando solo una estación,
        # pero como tiene una estacíon hijo se importará también.
        # Si una estación es hija de otra, solo podrá estar
        # dentro de la propiedad children, y no al nivel de stations

        try:
            imported_station_name = self.get_clonned_station_name(station['name'])

            imported_station = Station(name = imported_station_name, 
                                        id_ecoe = self.id,
                                        order = station['order'],
                                        id_parent_station = id_parent_station,
                                        id_manager=current_user.id)
            
            db.session.add(imported_station)
            db.session.flush()

            if len(station['children']) != 0:
                for child in station['children']: self.import_station(child, imported_station.id)

            imported_station.import_blocks(station['blocks'])

            db.session.commit()
            self.reorder_created_stations()
        except SQLAlchemyError:
            db.session.rollback()
            raise
        except Exception:
            db.session.rollback()
            raise