#  Copyright (c) 2020 Miguel Hernandez University of Elche
#  This file is part of openECOE-API.
#
#       openECOE-API is free software: you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation, either version 3 of the License, or
#       (at your option) any later version.
#
#       openECOE-API is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with openECOE-API.  If not, see <https://www.gnu.org/licenses/>.

"""Trabajos en segundo plano con RQ.

Sustituye a Flask-RQ2 (abandonada desde 2018) con lo que usa la aplicación:

* ``@rq.job(timeout=...)`` y ``funcion.queue(*args, **kwargs)`` para encolar,
* ``rq.get_queue()``, ``rq.set_task_progress()`` y ``rq.finish_job()``,
* el comando ``flask rq worker``.

Los trabajos se ejecutan dentro del contexto de la aplicación Flask. Si un trabajo falla, RQ lo vuelve a encolar
hasta ``TASK_MAX_TRIES`` veces (antes se hacía a mano en un manejador de excepciones).
"""
import logging
import os
from datetime import datetime
from functools import update_wrapper

import click
from redis import Redis
from rq import Queue, Retry, Worker, get_current_job
from rq.job import Job as RQJob

from app import flask_app

log = logging.getLogger(__name__)


class FlaskJob(RQJob):
    """Trabajo de RQ que se ejecuta con el contexto de la aplicación."""

    def perform(self):
        with flask_app.app_context():
            from app.model import db
            # El worker hace fork para cada trabajo: el hijo no debe reutilizar las conexiones del padre.
            db.engine.dispose(close=False)
            return super().perform()


class _QueuedFunction:
    def __init__(self, rq, func, timeout):
        self.rq = rq
        self.func = func
        self.timeout = timeout
        update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def queue(self, *args, **kwargs):
        return self.rq.get_queue().enqueue_call(
            self.func,
            args=args,
            kwargs=kwargs,
            timeout=self.timeout,
            retry=Retry(max=self.rq.TASK_MAX_TRIES),
        )


class OpenECOEQueue:
    TASK_MAX_TRIES = 15

    ARCHIVE_ROUTE = os.path.join(
        os.path.dirname(flask_app.instance_path),
        flask_app.config.get("DEFAULT_ARCHIVE_ROUTE"))

    if not os.path.exists(ARCHIVE_ROUTE):
        os.makedirs(ARCHIVE_ROUTE)

    def __init__(self, app):
        self.app = app
        self.default_queue = app.config.get("RQ_DEFAULT_QUEUE")
        self._connection = None

    @property
    def connection(self):
        if self._connection is None:
            self._connection = Redis.from_url(self.app.config["RQ_REDIS_URL"])
        return self._connection

    def get_queue(self, name=None):
        return Queue(name or self.default_queue, connection=self.connection, job_class=FlaskJob)

    def job(self, timeout=None):
        def decorator(func):
            return _QueuedFunction(self, func, timeout)
        return decorator

    @staticmethod
    def set_task_progress(progress):
        _task = get_current_job()
        if _task:
            _task.meta['progress'] = progress
            _task.save_meta()

    @staticmethod
    def finish_job(file=None):
        from app.model import Job
        from app.model import db
        OpenECOEQueue.set_task_progress(100)
        _task = get_current_job()
        task = db.session.get(Job, _task.id)
        if task:
            task.complete = True
            task.finished = datetime.now()
            if file:
                task.file = file
            db.session.commit()


def failed_job(job, exc_type, exc_value, traceback):
    retries_left = job.retries_left or 0
    if retries_left > 0:
        flask_app.logger.info("failed job %s scheduled for retry (%d left): %s", job.id, retries_left, exc_value)
    else:
        flask_app.logger.error("job %s failed permanently: %s", job.id, exc_value)
    return True  # sigue con el manejador por defecto de RQ (registro de fallidos y reintentos)


rq = OpenECOEQueue(flask_app)


@flask_app.cli.group("rq")
def rq_cli():
    """Trabajos en segundo plano (RQ)."""


@rq_cli.command("worker")
@click.option("--burst", is_flag=True, help="Sale cuando la cola se queda vacía.")
def rq_worker(burst):
    """Lanza un worker de RQ para la cola de openECOE."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    worker = Worker([rq.get_queue()], connection=rq.connection, job_class=FlaskJob,
                    exception_handlers=[failed_job])
    worker.work(burst=burst, with_scheduler=False)
