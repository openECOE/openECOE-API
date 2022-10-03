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
from enum import Enum

from flask_login import current_user
from flask_potion import fields, signals
from flask_potion.exceptions import BackendConflict, ItemNotFound
from flask_potion.instances import Instances
from flask_potion.routes import ItemRoute, Relation, Route
from werkzeug.exceptions import Forbidden

from app.api import export
from app.api._mainresource import MainManager, OpenECOEResource
from app.api.jobs import JobResource
from app.api.user import RoleType
from app.jobs import ecoe as jobs_ecoe
from app.jobs import statistics as jobs_statistics
from app.model.ECOE import ECOE, ChronoNotFound, ECOEstatus
from app.model.User import PermissionType
import os
from flask import send_from_directory, current_app
from app.statistics import generar_csv, resultados_evaluativo_ecoe
from app.auth import auth
class Location(int, Enum):
    ARCHIVE_ONLY = 1
    INSTANCES_ONLY = 2
    BOTH = 3


class ArchiveManager(MainManager):
    def _query(self, source=Location.INSTANCES_ONLY, **kwargs):
        query = super()._query(**kwargs)

        if query is None:
            return query
        elif source == Location.BOTH:
            return query
        elif source == Location.ARCHIVE_ONLY:
            return query.filter(getattr(self.model, "status") == ECOEstatus.ARCHIVED)
        else:
            return query.filter(getattr(self.model, "status") != ECOEstatus.ARCHIVED)

    def instances(self, where=None, sort=None, source=Location.INSTANCES_ONLY):
        query = self._query(source)
        if where:
            expressions = [
                self._expression_for_condition(condition) for condition in where
            ]
            query = self._query_filter(query, self._and_expression(expressions))
        if sort:
            query = self._query_order_by(query, sort)
        return query

    def archive_instances(self, page, per_page, where=None, sort=None):
        return self.instances(
            where=where, sort=sort, source=Location.ARCHIVE_ONLY
        ).paginate(page=page, per_page=per_page)

    def read(self, id, source=Location.INSTANCES_ONLY):
        query = self._query(source)
        if query is None:
            raise ItemNotFound(self.resource, id=id)
        return self._query_filter_by_id(query, id)


# Permissions to ECOE childs resources
class EcoeChildResource(OpenECOEResource):
    class Meta:
        #Tupla permiso:cadena_que_otorga_permiso
        permissions = {
            "read": ["read:ecoe", "evaluate"],
            "create": "manage",
            "update": "manage",
            "delete": "manage",
            "manage": [
                PermissionType.MANAGE + ":ecoe",
                PermissionType.MANAGE,
                RoleType.ADMIN,
            ],
            "evaluate": [
                PermissionType.EVALUATE + ":ecoe",
                PermissionType.EVALUATE,
                "manage",
            ],
        }


class EcoeResource(OpenECOEResource):
    areas = Relation("areas")
    stations = Relation("stations")
    schedules = Relation("schedules")
    students = Relation("students")
    rounds = Relation("rounds")
    shifts = Relation("shifts")
    stages = Relation("stages")

    class Meta:
        manager = ArchiveManager
        name = "ecoes"
        model = ECOE
        natural_key = "name"
        write_only_fields = ["user"]

        permissions = {
            "read": ["manage", "read", "evaluate"],
            "create": "update",
            "update": [RoleType.ADMIN, "manage"],
            "delete": "manage",
            "manage": [PermissionType.MANAGE, RoleType.SUPERADMIN, "user:user"],
            "evaluate": [PermissionType.EVALUATE, "manage"],
        }

        exclude_routes = ["destroy"]  # we're using rel="archive" instead.

    class Schema:
        organization = fields.ToOne("organizations", nullable=True)
        user = fields.ToOne("users", nullable=True)
        status = fields.String(enum=ECOEstatus, io="r")

    @staticmethod
    def get_ecoe_dict(ecoe):
        _dict_ecoe = {
            "ecoe": [ecoe],
            "area": ecoe.areas,
            "station": ecoe.stations,
            "shift": ecoe.shifts,
            "round": ecoe.rounds,
            "student": ecoe.students,
            "schedule": ecoe.schedules,
            "stages": ecoe.stages,
        }

        _blocks = []
        for station in ecoe.stations:
            _blocks += station.blocks
            _station_questions = {
                "station_%s-question" % station.order: station.questions
            }
            _dict_ecoe = {**_dict_ecoe, **_station_questions}

        _dict_ecoe["block"] = _blocks

        for schedule in ecoe.schedules:
            _schedule_events = {"schedule_%s-event" % schedule.id: schedule.events}
            _dict_ecoe = {**_dict_ecoe, **_schedule_events}

        _student_answers = []
        for student in ecoe.students:
            _student_answers += student.answers

        _dict_ecoe["answers"] = _student_answers

        return _dict_ecoe
    '''
    @ItemRoute.GET(
        "/export", rel="exportItem", description="export all ECOE data to file"
    )
    def export_ecoe(self, ecoe):
        
        #relativefilepath = generar_csv(ecoe=id_ecoe)
        #return send_file(relativefilepath, as_attachment=True)
        # Only can export if have manage permissions
        object_permissions = self.manager.get_permissions_for_item(ecoe)
        if "manage" in object_permissions and object_permissions["manage"] is not True:
            raise Forbidden

        return export.book_dict(self.get_ecoe_dict(ecoe), filename=ecoe.name)
    '''
    ##################### AQUI VAMOS A HACER LAS PRUEBAS PARA PASAR A JOBS LA GENERACIÓN DE CSV     ########
    #Lanza de forma sincrona, funciona
    @ItemRoute.GET(
        "/export2", rel="exportItem", description="export all ECOE data to file"
    )
    def export_ecoe(self, ecoe):
        object_permissions = self.manager.get_permissions_for_item(ecoe)
        if "manage" in object_permissions and object_permissions["manage"] is not True:
            raise Forbidden

        file_path = os.path.join(os.path.dirname(current_app.instance_path), current_app.config.get("DEFAULT_ARCHIVE_ROUTE"))
        file_name = generar_csv(ecoe=str(ecoe.id))
        return send_from_directory(directory=file_path,
                                    filename=file_name,
                                    as_attachment=True)

    #Recoge los datos del trabajo
    @ItemRoute.GET("/export3")
    def get_opendata3(self, ecoe) -> fields.List(fields.Inline(JobResource)):
        # Only can get data if have manage permissions
        object_permissions = self.manager.get_permissions_for_item(ecoe)
        if "manage" in object_permissions and object_permissions["manage"] is not True:
            raise Forbidden

        job = current_user.jobs.filter_by(
            #TODO:: Esto es una función customizada que se gestiona en el módulo jobs, cambiar la ruta al 
            name="app.jobs.statistics.export_csv(ecoe=%s, identidad=%s)" % (ecoe.id, auth.current_user.id)
        )
        return job
    #Genera el trabajo y lo lanza en segundo plano
    @ItemRoute.POST("/export3")
    def gen_opendata3(self, ecoe) -> fields.Inline(JobResource):
        # Only can get data if have manage permissions
        object_permissions = self.manager.get_permissions_for_item(ecoe)
        if "manage" in object_permissions and object_permissions["manage"] is not True:
            raise Forbidden

        
        _identidad = str(auth.current_user.id)
        _job = current_user.launch_job(
            func=jobs_statistics.export_csv,
            description="Export3 Lanzamiento prueba 2 %s" % ecoe.name,
            ecoe=str(ecoe.id),
            identidad=_identidad,
        )

        return _job                                
    #########################################################################################################
    @Route.GET("/export", rel="export", description="export all ECOE data to file")
    def export_ecoes(self):
        # Only can export if have manage permissions
        object_permissions = self.manager.get_permissions_for_item(self)
        if "manage" in object_permissions and object_permissions["manage"] is not True:
            raise Forbidden

        _ecoes = self.manager.instances().all()

        _dict = {}

        for _ecoe in _ecoes:
            _dict_ecoe = {
                "ecoe_%s-%s" % (_ecoe.id, key): item
                for key, item in self.get_ecoe_dict(_ecoe).items()
            }
            _dict = {**_dict, **_dict_ecoe}

        return export.book_dict(_dict, filename="ECOE")

    #Recoge los datos del trabajo
    @ItemRoute.GET("/opendata", rel="getOpenDataJobs")
    def get_opendata(self, ecoe) -> fields.List(fields.Inline(JobResource)):
        # Only can get data if have manage permissions
        object_permissions = self.manager.get_permissions_for_item(ecoe)
        if "manage" in object_permissions and object_permissions["manage"] is not True:
            raise Forbidden

        return current_user.jobs.filter_by(
            name="app.jobs.ecoe.export_data(id_ecoe=%s)" % ecoe.id
        )
        
        
    #Genera el trabajo y lo lanza en segundo plano
    @ItemRoute.POST("/opendata", rel="generateOpenData")
    def gen_opendata(self, ecoe) -> fields.Inline(JobResource):
        # Only can get data if have manage permissions
        object_permissions = self.manager.get_permissions_for_item(ecoe)
        if "manage" in object_permissions and object_permissions["manage"] is not True:
            raise Forbidden
                
        _job = current_user.launch_job(
            func=jobs_ecoe.export_data,
            description="Export %s opendata" % ecoe.name,
            id_ecoe=ecoe.id,
        )

        return _job
    
    @ItemRoute.GET("/csv", rel='getecoe')
    def send_CSV_ecoe(self, ecoe):
        object_permissions = self.manager.get_permissions_for_item(ecoe)
        if "manage" in object_permissions and object_permissions["manage"] is not True:
            raise Forbidden
        
        file_path = os.path.join(os.path.dirname(current_app.instance_path), current_app.config.get("DEFAULT_ARCHIVE_ROUTE"))
        file_name = generar_csv(ecoe=str(ecoe.id))
        return send_from_directory(directory=file_path,
                                    filename=file_name,
                                    as_attachment=True)

    @ItemRoute.GET("/results", rel='resultados_evaluativo_ecoe')
    def send_evaluativo_ecoe(self, ecoe):
        object_permissions = self.manager.get_permissions_for_item(ecoe)
        if "manage" in object_permissions and object_permissions["manage"] is not True:
            raise Forbidden
        return resultados_evaluativo_ecoe(ecoe=str(ecoe.id))
        
    @ItemRoute.GET("/configuration", rel="chronoSchema")
    def configuration(self, ecoe) -> fields.String():
        return ecoe.configuration

    @ItemRoute.POST("/start", rel="startChrono")
    def chrono_start(self, ecoe) -> fields.String():
        return ecoe.start()

    @ItemRoute.POST("/play", rel="playChrono")
    def chrono_play(self, ecoe) -> fields.String():
        return ecoe.play()

    @ItemRoute.POST("/pause", rel="pauseChrono")
    def chrono_pause(self, ecoe) -> fields.String():
        return ecoe.pause()

    @ItemRoute.POST("/abort", rel="abortChrono")
    def chrono_abort(self, ecoe) -> fields.String():
        return ecoe.abort()

    @ItemRoute.POST("/load", rel="loadChrono")
    def chrono_load(self, ecoe) -> fields.String():
        return ecoe.load_config()

    @ItemRoute.POST("/publish", rel="publish")    
    def publish(self, ecoe) -> fields.Inline("self"):
        item = self.manager.read(ecoe.id, source=Location.INSTANCES_ONLY)
        return self.manager.update(item, {"status": ECOEstatus.PUBLISHED})

    @ItemRoute.POST("/draft", rel="draft")
    def draft(self, ecoe) -> fields.Inline("self"):
        item = self.manager.read(ecoe.id, source=Location.INSTANCES_ONLY)
        return self.manager.update(item, {"status": ECOEstatus.DRAFT})

    @Route.GET("/<int:id>", rel="self", attribute="instance")
    def read(self, id) -> fields.Inline("self"):
        return self.manager.read(id, source=Location.BOTH)

    @read.PATCH(rel="update", attribute="instance")
    def update(self, properties, id):
        item = self.manager.read(id, source=Location.INSTANCES_ONLY)
        updated_item = self.manager.update(item, properties)
        return updated_item

    update.response_schema = update.request_schema = fields.Inline(
        "self", patchable=True
    )

    @update.DELETE(rel="archive")
    def destroy(self, id):
        item = self.manager.read(id, source=Location.INSTANCES_ONLY)
        self.manager.update(item, {"status": ECOEstatus.ARCHIVED})
        return None, 204

    @Route.GET("/archive")
    def archive_instances(self, **kwargs):
        return self.manager.archive_instances(**kwargs)

    archive_instances.request_schema = archive_instances.response_schema = Instances()

    @Route.GET("/archive/<int:id>", rel="readArchived")
    def read_archive(self, id) -> fields.Inline("self"):
        return self.manager.read(id, source=Location.ARCHIVE_ONLY)

    @Route.POST("/archive/<int:id>/restore", rel="restoreFromArchive")
    def restore_from_archive(self, id) -> fields.Inline("self"):
        item = self.manager.read(id, source=Location.ARCHIVE_ONLY)
        return self.manager.update(item, {"status": ECOEstatus.DRAFT})


# Add permissions to manage to creator
@signals.before_create.connect_via(EcoeResource)
def before_create_ecoe(sender, item):
    if not item.organization:
        item.organization = current_user.organization

    if not item.user:
        item.user = current_user


# Update ECOE
@signals.before_update.connect_via(EcoeResource)
def before_update_ecoe(sender, item, changes):
    if "status" in changes.keys():
        if changes["status"] == ECOEstatus.PUBLISHED:
            try:
                item.load_config()
            except ChronoNotFound:
                pass
        elif changes["status"] in (ECOEstatus.DRAFT, ECOEstatus.ARCHIVED):
            try:
                if item.chrono_token:
                    item.delete_config()
            except (ChronoNotFound, BackendConflict):
                pass
