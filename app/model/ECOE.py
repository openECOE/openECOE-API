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
from flask_potion.exceptions import BackendConflict, PageNotFound
from sqlalchemy.dialects import mysql

from app.model import db


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
