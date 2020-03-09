"""Questions JSON Format

Revision ID: 5126c6c1a838
Revises: 966e0a3b6e33
Create Date: 2020-03-04 13:35:07.398500

"""
#  Copyright (c) 2020 Miguel Hernandez University of Elche
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

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy import table, select
import json

# revision identifiers, used by Alembic.
revision = '5126c6c1a838'
down_revision = '966e0a3b6e33'
branch_labels = None
depends_on = None

def upgrade():
    question_type_dict = {'RANGE_SELECT': 'range', 'RADIO_BUTTON': 'radio', 'CHECK_BOX': 'checkbox'}

    conn = op.get_bind()

    # # ### commands auto generated by Alembic - please adjust! ###
    block = op.create_table('block',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_station', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=300), nullable=True),
    sa.Column('order', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_station'], ['station.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    # ### migrate data from qblock to block
    results = conn.execute("select id, id_station, name, `order` from qblock").fetchall()
    qblocks = [{'id': r[0], 'id_station': r[1], 'name': r[2], 'order': r[3]} for r in results]

    op.bulk_insert(block, qblocks)

    answer = op.create_table('answer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_student', sa.Integer(), nullable=False),
    sa.Column('id_question', sa.Integer(), nullable=False),
    sa.Column('answer_schema', mysql.LONGTEXT(), nullable=True),
    sa.Column('points', sa.Numeric(10,2), nullable=True),
    sa.ForeignKeyConstraint(['id_student'], ['student.id'], ),
    sa.ForeignKeyConstraint(['id_question'], ['question.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_student', 'id_question', name='answer_student_question_uk'),
    sa.CheckConstraint('answer_schema IS NULL OR JSON_VALID(answer_schema)')
    )

    # ### migrate data from student_options to answer
    results = conn.execute("select so.student_id, q.id, q.question_type, \
                            GROUP_CONCAT(o.order) as opt_order, GROUP_CONCAT(o.id) as id_opt, sum(o.points) as points \
                            from question q, `option` o, students_options so \
                            where q.id = o.id_question \
                            and so.option_id = o.id \
                            group by so.student_id, q.id, q.question_type \
                            order by so.student_id, q.id, o.order;").fetchall()

    students_options = []

    for r in results:
        type_ = question_type_dict[r['question_type']]

        if type_ == 'radio':
            option_selected = {'id_option': r['id_opt']}
        elif type_ == 'range':
            option_selected = r['opt_order']
        else:
            option_selected = [ {'id_option': o}
                                for o in r['id_opt'].split(',')]

        answer_schema_ = {"type": type_,
                          "selected": option_selected}

        students_options.append({'id_student': r['student_id'], 'id_question': r['id'], 'answer_schema': json.dumps(answer_schema_), 'points': r['points']})

    op.bulk_insert(answer, students_options)

    op.alter_column('ecoe', 'status',
               existing_type=mysql.ENUM('ARCHIVED', 'DRAFT', 'PUBLISHED', collation='latin1_general_ci'),
               nullable=False)
    op.add_column('question', sa.Column('id_block', sa.Integer(), nullable=True))
    op.add_column('question', sa.Column('id_station', sa.Integer(), nullable=False))
    op.add_column('question', sa.Column('question_schema', mysql.LONGTEXT(), nullable=False))
    op.create_check_constraint(
        "ck_question_json",
        "question",
        "question_schema IS NULL OR JSON_VALID(question_schema)"
    )
    op.alter_column('question', 'order',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)

    ### migrate data from qblocks_questions to question
    question = table(
        'question',
        sa.Column('id', sa.Integer()),
        sa.Column('id_block', sa.Integer()),
        sa.Column('id_station', sa.Integer()),
        sa.Column('question_schema', mysql.LONGTEXT()),
        # Other columns not needed for the data migration
    )

    qblock = table(
        'qblock',
        sa.Column('id', sa.Integer()),
        sa.Column('id_station', sa.Integer()))

    qblocks_questions = table(
        'qblocks_questions',
        sa.Column('qblock_id', sa.Integer()),
        sa.Column('question_id', sa.Integer()))

    op.execute(question.update().values(
        id_block=select([qblocks_questions.c.qblock_id]). \
            where(qblocks_questions.c.question_id == question.c.id)
    ))

    op.execute(question.update().values(
        id_station=select([qblock.c.id_station]). \
            where(qblock.c.id == question.c.id_block)
    ))

    op.create_foreign_key('fk_question_block', 'question', 'block', ['id_block'], ['id'])
    op.create_foreign_key('fk_question_station', 'question', 'station', ['id_station'], ['id'])

    # ### Import options to new model
    results = conn.execute("select q.id, q.question_type, q.reference, q.description \
                            from question q").fetchall()
    for r in results:
        id_question_ = r[0]
        type_ = question_type_dict[r[1]]

        options = conn.execute("select o.id, o.label, o.points, o.order, false as selected \
                                from `option` o \
                                where o.id_question = %(id_q)s order by o.order" % {'id_q': id_question_}
                                ).fetchall()

        question_options = [
            {'id_option': o[0], 'label': o[1], 'points': str(o[2]), 'order': o[3]}
            for o in options]

        if type_ == 'range':
            range_ = len(question_options)
            points_ = question_options[-1]['points']
            question_schema_ = {'type': type_, 'reference': r[2], 'description': r[3], 'range': range_, 'points': str(points_)}
        else:
            question_schema_ = {'type': type_, 'reference': r[2], 'description': r[3], 'options': question_options}

        op.execute(question.update()
                   .where(question.c.id == id_question_)
                   .values(question_schema=json.dumps(question_schema_)))


    op.drop_table('qblocks_questions')
    op.drop_table('students_options')
    op.drop_table('option')
    op.drop_table('qblock')


    op.drop_column('question', 'question_type')
    op.drop_column('question', 'description')
    op.drop_column('question', 'reference')
    # ### end Alembic commands ###


def downgrade():
    question_type_dict = {'range' : 'RANGE_SELECT', 'radio' : 'RADIO_BUTTON', 'checkbox' : 'CHECK_BOX'}

    conn = op.get_bind()

    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('question', sa.Column('reference', mysql.VARCHAR(collation='latin1_general_ci', length=100), nullable=True))
    op.add_column('question', sa.Column('description', mysql.VARCHAR(collation='latin1_general_ci', length=500), nullable=True))
    op.add_column('question', sa.Column('question_type', mysql.ENUM('RADIO_BUTTON', 'CHECK_BOX', 'RANGE_SELECT', collation='latin1_general_ci'), nullable=False))
    op.drop_constraint('fk_question_block', 'question', type_='foreignkey')
    op.drop_constraint('fk_question_station', 'question', type_='foreignkey')
    op.alter_column('question', 'order',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)

    op.alter_column('ecoe', 'status',
               existing_type=mysql.ENUM('ARCHIVED', 'DRAFT', 'PUBLISHED', collation='latin1_general_ci'),
               nullable=True)
    option = op.create_table('option',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('points', mysql.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('label', mysql.VARCHAR(collation='latin1_general_ci', length=255), nullable=True),
    sa.Column('id_question', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('order', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['id_question'], ['question.id'], name='option_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='latin1_general_ci',
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )

    # ### Import questions and options from JSON to relational model
    question = table(
        'question',
        sa.Column('id', sa.Integer()),
        sa.Column('id_block', sa.Integer()),
        sa.Column('id_station', sa.Integer()),
        sa.Column('reference', mysql.VARCHAR(collation='latin1_general_ci', length=100), nullable=True),
        sa.Column('description', mysql.VARCHAR(collation='latin1_general_ci', length=500), nullable=True),
        sa.Column('question_type',
                  mysql.ENUM('RADIO_BUTTON', 'CHECK_BOX', 'RANGE_SELECT', collation='latin1_general_ci'),
                  nullable=False),
        sa.Column('question_schema', mysql.LONGTEXT()),
        # Other columns not needed for the data migration
    )

    results = conn.execute("select q.id, q.question_schema, q.id_block \
                                from question q").fetchall()
    options_ = []
    options_range_ = []
    qblocks_questions_ = []
    for r in results:
        id_question_ = r['id']
        question_schema_ = json.loads(r['question_schema'])

        op.execute(question.update()
                   .where(question.c.id == id_question_)
                   .values(question_type=question_type_dict[question_schema_["type"]],
                           reference=question_schema_["reference"],
                           description=question_schema_["description"]))

        qblocks_questions_.append({"qblock_id": r['id_block'], "question_id": id_question_})

        if question_schema_["type"] == 'range':
            for v in range(1, question_schema_["range"] + 1):
                points_ = (round(float(question_schema_["points"]), 2) / question_schema_["range"]) * v
                options_range_.append({"points": points_, "label": str(v), "id_question": id_question_, "order": v})
        else:
            for o in question_schema_["options"]:
                options_.append({"id" : o["id_option"], "points" : o["points"], "label": o["label"], "id_question": id_question_, "order" : o["order"]})

    op.bulk_insert(option, options_)
    op.bulk_insert(option, options_range_)

    qblock = op.create_table('qblock',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('name', mysql.VARCHAR(collation='latin1_general_ci', length=300), nullable=True),
    sa.Column('id_station', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('order', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['id_station'], ['station.id'], name='qblock_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='latin1_general_ci',
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )

    # ### migrate data from qblock to block
    results = conn.execute("select id, id_station, name, `order` from block").fetchall()
    blocks_ = [{'id': r[0], 'id_station': r[1], 'name': r[2], 'order': r[3]} for r in results]
    op.bulk_insert(qblock, blocks_)

    qblocks_questions = op.create_table('qblocks_questions',
    sa.Column('qblock_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('question_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['qblock_id'], ['qblock.id'], name='qblocks_questions_ibfk_1'),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], name='qblocks_questions_ibfk_2'),
    sa.PrimaryKeyConstraint('qblock_id', 'question_id'),
    mysql_collate='latin1_general_ci',
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    # ### migrate data from question blocks
    op.bulk_insert(qblocks_questions, qblocks_questions_)

    students_options = op.create_table('students_options',
    sa.Column('student_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('option_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['option_id'], ['option.id'], name='students_options_ibfk_1'),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], name='students_options_ibfk_2'),
    sa.PrimaryKeyConstraint('student_id', 'option_id'),
    mysql_collate='latin1_general_ci',
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )

    results = conn.execute("select id, id_student, id_question, answer_schema, points from answer").fetchall()


    answers = []
    for r in results:
        id_student_ = r['id_student']
        id_question_ = r['id_question']
        points_ = r['points']
        answer_schema_ = json.loads(r['answer_schema'])

        if answer_schema_["type"] == 'range':
            results = conn.execute("select id from option where id_question= %(id_q)s \
                                   and `points` = %(points)s"% {"id_q": id_question_, "points": points_}).fetchall()

            option_ = results[0]["id"]

            answers.append({'student_id': id_student_, 'option_id': option_})
        elif answer_schema_["type"] == 'radio':
            answers.append({'student_id': id_student_, 'option_id': answer_schema_["selected"]["id_option"]})
        else:
            for o in answer_schema_["selected"]:
                answers.append({'student_id': id_student_, 'option_id': o["id_option"]})

    op.bulk_insert(students_options, answers)


    # ### Drop tables and columns
    op.drop_table('answer')
    op.drop_table('block')

    op.drop_column('question', 'question_schema')
    op.drop_column('question', 'id_station')
    op.drop_column('question', 'id_block')
    # ### end Alembic commands ###
