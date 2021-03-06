"""Create Tables

Revision ID: 8051e2b3a2d8
Revises: 
Create Date: 2018-05-14 13:32:08.483288

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8051e2b3a2d8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('organization',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('stage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.Column('order', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ecoe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('id_organization', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_organization'], ['organization.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('registered_on', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('surname', sa.String(length=255), nullable=True),
    sa.Column('is_superadmin', sa.Boolean(), nullable=False),
    sa.Column('token', sa.String(length=255), nullable=True),
    sa.Column('token_expiration', sa.DateTime(), nullable=True),
    sa.Column('id_organization', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_organization'], ['organization.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_token'), 'user', ['token'], unique=True)
    op.create_table('area',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('id_ecoe', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_ecoe'], ['ecoe.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', 'id_ecoe', name='area_ecoe_uk')
    )
    op.create_table('round',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_ecoe', sa.Integer(), nullable=True),
    sa.Column('round_code', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['id_ecoe'], ['ecoe.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('round_code', 'id_ecoe', name='round_ecoe_uk')
    )
    op.create_table('shift',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_ecoe', sa.Integer(), nullable=True),
    sa.Column('shift_code', sa.String(length=20), nullable=False),
    sa.Column('time_start', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['id_ecoe'], ['ecoe.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('shift_code', 'id_ecoe', name='shift_ecoe_uk')
    )
    op.create_table('station',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('id_ecoe', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_ecoe'], ['ecoe.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', 'id_ecoe', name='station_ecoe_uk')
    )
    op.create_table('planner',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_shift', sa.Integer(), nullable=False),
    sa.Column('id_round', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_round'], ['round.id'], ),
    sa.ForeignKeyConstraint(['id_shift'], ['shift.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_shift', 'id_round', name='shift_round_uk')
    )
    op.create_table('qblock',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('id_station', sa.Integer(), nullable=False),
    sa.Column('order', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_station'], ['station.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('reference', sa.String(length=50), nullable=True),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('id_area', sa.Integer(), nullable=False),
    sa.Column('question_type', sa.Enum('RADIO_BUTTON', 'CHECK_BOX', name='qtype'), nullable=False),
    sa.ForeignKeyConstraint(['id_area'], ['area.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('schedule',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_ecoe', sa.Integer(), nullable=True),
    sa.Column('id_stage', sa.Integer(), nullable=False),
    sa.Column('id_station', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_ecoe'], ['ecoe.id'], ),
    sa.ForeignKeyConstraint(['id_stage'], ['stage.id'], ),
    sa.ForeignKeyConstraint(['id_station'], ['station.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_ecoe', 'id_stage', name='ecoe_stage_uk'),
    sa.UniqueConstraint('id_station', 'id_stage', name='station_stage_uk')
    )
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time', sa.Integer(), nullable=False),
    sa.Column('sound', sa.String(length=550), nullable=True),
    sa.Column('text', sa.String(length=255), nullable=True),
    sa.Column('id_schedule', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_schedule'], ['schedule.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('option',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.Column('label', sa.String(length=255), nullable=True),
    sa.Column('id_question', sa.Integer(), nullable=False),
    sa.Column('order', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_question'], ['question.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('qblocks_questions',
    sa.Column('qblock_id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['qblock_id'], ['qblock.id'], ),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.PrimaryKeyConstraint('qblock_id', 'question_id')
    )
    op.create_table('student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('surnames', sa.String(length=100), nullable=False),
    sa.Column('dni', sa.String(length=10), nullable=True),
    sa.Column('id_ecoe', sa.Integer(), nullable=False),
    sa.Column('id_planner', sa.Integer(), nullable=True),
    sa.Column('planner_order', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_ecoe'], ['ecoe.id'], ),
    sa.ForeignKeyConstraint(['id_planner'], ['planner.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', 'surnames', 'id_ecoe', name='student_name_ecoe_uk')
    )
    op.create_table('students_options',
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('option_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['option_id'], ['option.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('student_id', 'option_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('students_options')
    op.drop_table('student')
    op.drop_table('qblocks_questions')
    op.drop_table('option')
    op.drop_table('event')
    op.drop_table('schedule')
    op.drop_table('question')
    op.drop_table('qblock')
    op.drop_table('planner')
    op.drop_table('station')
    op.drop_table('shift')
    op.drop_table('round')
    op.drop_table('area')
    op.drop_index(op.f('ix_user_token'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('ecoe')
    op.drop_table('stage')
    op.drop_table('organization')
    # ### end Alembic commands ###
