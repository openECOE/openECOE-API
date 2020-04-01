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

from app import flask_app
from flask_rq2 import RQ
from rq import get_current_job
from datetime import timedelta, datetime
import logging
log = logging.getLogger(__name__)


class OpenECOEQueue(RQ):
    TASK_RETRY = 'fail-count'
    TASK_MAX_TRIES = 15
    TASK_RETRY_DELAY = timedelta(seconds=12)
    TASK_STACKTRACE = False

    def start_service(self):
        worker = self.get_worker()
        worker.work()

    def clear_crons(self):
        scheduler = self.get_scheduler()
        [scheduler.cancel(job) for job in scheduler.get_jobs()]

    @staticmethod
    def set_task_progress(progress):
        _task = get_current_job()
        if _task:
            _task.meta['progress'] = progress
            _task.save_meta()
            # task.user.add_notification('task_progress', {'task_id': job.get_id(),
            #                                              'progress': progress})

    @staticmethod
    def finish_job(file=None):
        from app.model import Job
        from app.model import db
        OpenECOEQueue.set_task_progress(100)
        _task = get_current_job()
        task = Job.query.get(_task.get_id())
        if task:
            task.complete = True
            task.finished = datetime.now()
            if file:
                task.file = file
            db.session.commit()


rq = OpenECOEQueue(flask_app)
rq.default_queue = flask_app.config.get('RQ_DEFAULT_QUEUE')


@rq.exception_handler
def failed_job(job, *exc_info):

    fail_count = job.meta[rq.TASK_RETRY] if rq.TASK_RETRY in job.meta else 0
    if fail_count < rq.TASK_MAX_TRIES:

        fail_count += 1
        job.meta[rq.TASK_RETRY] = fail_count
        job.save_meta()
        job.requeue()
        flask_app.logger.info("failed job %s scheduled for retry %d/%d" % (job.id, fail_count, rq.TASK_MAX_TRIES))

    else:

        job.meta[rq.TASK_RETRY] = 0
        job.save_meta()
        flask_app.logger.error("job %s failed permanently" % job.id)


if __name__ == '__main__':
    rq.clear_crons()
    rq.start_service()
