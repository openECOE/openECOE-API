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
import datetime
import os

from flask import current_app, json
from app.jobs import rq


def clean_html(text):
    """Remove html tags from a string"""
    import re
    """First replace <br> with spaces"""

    br_space = re.compile('<?br.*?>')
    clean = re.compile('<.*?>')

    text = re.sub(br_space, ' ', text)
    return re.sub(clean, '', text)


@rq.job(timeout=300)
def export_data(id_ecoe):
    from zipfile import ZipFile, ZIP_DEFLATED
    from app.model.Student import Answer
    from app.model.ECOE import ECOE
    import app.api.export as export


    dummy_answer = Answer(points='0.00', answer_schema='{}')

    _ecoe = ECOE.query.get(id_ecoe)

    _data = []

    _count_students = len(_ecoe.students)
    _count_questions = sum([len(station.questions) for station in _ecoe.stations])

    _count_total = _count_students * _count_questions
    _count = 0

    rq.set_task_progress(0)
    for student in _ecoe.students:
        _tuple = {'ecoe_name': _ecoe.name,
                  'shift_time_start': student.planner.shift.time_start,
                  'round_description': student.planner.round.description,
                  'student_order': student.planner_order,
                  'student_dni': student.dni,
                  'student_name': student.name,
                  'student_surnames': student.surnames,
                  'shift_code': student.planner.shift.shift_code,
                  'round_code': student.planner.round.round_code}

        for station in _ecoe.stations:
            _tuple = {**_tuple,
                      'station_order': station.order,
                      'station_name': station.name}

            for question in station.questions:
                _question = json.loads(question.question_schema)

                _tuple = {**_tuple,
                          'question_order': question.order,
                          'question_type': _question['type'],
                          'question_description': clean_html(_question['description']),
                          'question_reference': clean_html(_question['reference']),
                          'question_max_points': str(question.max_points),
                          'area_code': question.area.code,
                          'area_name': question.area.name}

                _answers = set(student.answers).intersection(question.answers)

                if len(_answers) == 0:
                    _answers = [dummy_answer]

                for answer in _answers:
                    def search_in_options(list_options, id_option):
                        for option in list_options:
                            if str(option['id_option']) == str(id_option):
                                return clean_html(option['label'])
                        return ''

                    _answer = json.loads(answer.answer_schema)
                    _answers_list = []

                    if 'selected' in _answer:
                        if isinstance(_answer['selected'], list):
                            for option_selected in _answer['selected']:
                                _answers_list.append(search_in_options(_question['options'],
                                                                       option_selected['id_option']))
                        elif isinstance(_answer['selected'], dict):
                            _answers_list.append(search_in_options(_question['options'],
                                                                   _answer['selected']['id_option']))
                        elif isinstance(_answer['selected'], int):
                            _answers_list.append(str(_answer['selected']))

                    _tuple = {**_tuple,
                              'answer_points': str(answer.points),
                              'answer_selected': " # ".join(_answers_list)}

                    _data.append(_tuple)

                    _count += 1
                    rq.set_task_progress(round(99 * _count // _count_total))

    _filename = 'opendata_%s_%s' % (_ecoe.name, datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    _filetype = 'csv'

    _file = export.records(_records=_data,
                           filename=_filename,
                           filetype=_filetype)

    _archiveroute = os.path.join(os.path.dirname(current_app.instance_path),
                                 current_app.config.get("DEFAULT_ARCHIVE_ROUTE"),
                                 _filename)

    with open('%s.%s' % (_archiveroute, _filetype), 'wb') as f:
        f.write(_file.data)
        f.flush()

        with ZipFile('%s.zip' % _archiveroute, "w") as zf:
            zf.write(f.name, arcname='%s.%s' % (_filename, _filetype), compress_type=ZIP_DEFLATED)
            zf.close()
        f.close()
        os.remove(f.name)
        rq.finish_job(file='%s.zip' % _filename)

