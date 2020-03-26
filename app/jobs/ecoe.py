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

# Creates a worker that handle jobs in ``default`` queue.
from flask import current_app, json

from app import rq
from app.jobs._job import set_job_progress


@rq.job
def export_data(id_ecoe):
    from zipfile import ZipFile, ZIP_DEFLATED
    import datetime
    import os
    from app.model.Student import Answer
    from app.model.ECOE import ECOE
    import app.api.export as export

    dummy_answer = Answer(points='', answer_schema='{}')

    _ecoe = ECOE.query.get(id_ecoe)

    _data = []

    _count_students = len(_ecoe.students)
    _count_questions = sum([len(station.questions) for station in _ecoe.stations])

    _count_total = _count_students * _count_questions

    _count = 0
    set_job_progress(0)
    for student in _ecoe.students:
        _tuple = {'ecoe_name': _ecoe.name,
                  'shift_time_start': student.planner.shift.time_start,
                  'round_description': student.planner.round.description,
                  'student_order': student.planner_order,
                  'student_dni': student.dni,
                  'student_name': '%s, %s' % (student.surnames, student.name),
                  'shift_code': student.planner.shift.shift_code,
                  'round_code': student.planner.round.round_code}

        for station in _ecoe.stations:
            _tuple = {**_tuple,
                      'station_order': station.order,
                      'station_name': station.name}

            for question in station.questions:
                _tuple = {**_tuple,
                          'question_order': question.order,
                          'question_schema': json.loads(question.question_schema),
                          'question_max_points': str(question.max_points),
                          'area_code': question.area.code,
                          'area_name': question.area.name}

                _answers = set(student.answers).intersection(question.answers)

                if len(_answers) == 0:
                    _answers = [dummy_answer]

                for answer in _answers:
                    _tuple = {**_tuple,
                              'answer_schema': json.loads(answer.answer_schema),
                              'answer_points': str(answer.points)}
                    _data.append(_tuple)

                    _count += 1
                    set_job_progress(100* _count // _count_total)

    _filename = 'opendata_%s_%s' % (_ecoe.name, datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    _filetype = 'csv'

    _saveroute = current_app.config.get("DEFAULT_ARCHIVE_ROUTE")

    _file = export.records(_records=_data,
                           filename=_filename,
                           filetype='csv')

    with open('%s.%s' % (_filename, _filetype), 'wb') as f:
        f.write(_file.data)
        f.flush()

        with ZipFile('%s/%s.zip' % (_saveroute, _filename), "w") as zf:
            zf.write(f.name, compress_type=ZIP_DEFLATED, )
            zf.close()
        f.close()
        os.remove(f.name)

    return _file
