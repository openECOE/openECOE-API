"""empty message

Revision ID: d99d8678f79b
Revises: 4753349d9328
Create Date: 2018-04-20 07:29:06.669449

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd99d8678f79b'
down_revision = '4753349d9328'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chronometer',
    sa.Column('id_chronometer', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('total_time', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id_chronometer')
    )
    op.create_table('organization',
    sa.Column('id_organization', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id_organization')
    )
    op.create_table('alarm',
    sa.Column('id_alarm', sa.Integer(), nullable=False),
    sa.Column('time', sa.Integer(), nullable=False),
    sa.Column('sound', sa.String(length=550), nullable=False),
    sa.Column('id_chronometer', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_chronometer'], ['chronometer.id_chronometer'], ),
    sa.PrimaryKeyConstraint('id_alarm')
    )
    op.create_table('ecoe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('id_organization', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_organization'], ['organization.id_organization'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('area',
    sa.Column('id_area', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=257), nullable=True),
    sa.Column('id_ecoe', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_ecoe'], ['ecoe.id'], ),
    sa.PrimaryKeyConstraint('id_area')
    )
    op.create_table('day',
    sa.Column('id_day', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('id_ecoe', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_ecoe'], ['ecoe.id'], ),
    sa.PrimaryKeyConstraint('id_day')
    )
    op.create_table('ecoe_chrono',
    sa.Column('id_ecoe', sa.Integer(), nullable=False),
    sa.Column('id_chronometer', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_chronometer'], ['chronometer.id_chronometer'], ),
    sa.ForeignKeyConstraint(['id_ecoe'], ['ecoe.id'], ),
    sa.PrimaryKeyConstraint('id_ecoe', 'id_chronometer')
    )
    op.create_table('station',
    sa.Column('id_station', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('id_ecoe', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_ecoe'], ['ecoe.id'], ),
    sa.PrimaryKeyConstraint('id_station')
    )
    op.create_table('group',
    sa.Column('id_group', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('id_station', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_station'], ['station.id_station'], ),
    sa.PrimaryKeyConstraint('id_group')
    )
    op.create_table('shift',
    sa.Column('id_shift', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DATETIME(), nullable=True),
    sa.Column('id_day', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_day'], ['day.id_day'], ),
    sa.PrimaryKeyConstraint('id_shift')
    )
    op.create_table('station_chrono',
    sa.Column('id_station', sa.Integer(), nullable=False),
    sa.Column('id_chronometer', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_chronometer'], ['chronometer.id_chronometer'], ),
    sa.ForeignKeyConstraint(['id_station'], ['station.id_station'], ),
    sa.PrimaryKeyConstraint('id_station', 'id_chronometer')
    )
    op.create_table('question',
    sa.Column('id_question', sa.Integer(), nullable=False),
    sa.Column('id_group', sa.Integer(), nullable=False),
    sa.Column('id_area', sa.Integer(), nullable=False),
    sa.Column('wording', sa.String(length=500), nullable=True),
    sa.Column('option_type', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['id_area'], ['area.id_area'], ),
    sa.ForeignKeyConstraint(['id_group'], ['group.id_group'], ),
    sa.PrimaryKeyConstraint('id_question')
    )
    op.create_table('round',
    sa.Column('id_round', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('id_shift', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_shift'], ['shift.id_shift'], ),
    sa.PrimaryKeyConstraint('id_round')
    )
    op.create_table('option',
    sa.Column('id_option', sa.Integer(), nullable=False),
    sa.Column('points', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('id_question', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_question'], ['question.id_question'], ),
    sa.PrimaryKeyConstraint('id_option')
    )
    op.create_table('student',
    sa.Column('id_student', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('dni', sa.String(length=25), nullable=True),
    sa.Column('id_ecoe', sa.Integer(), nullable=False),
    sa.Column('id_round', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_ecoe'], ['ecoe.id'], ),
    sa.ForeignKeyConstraint(['id_round'], ['round.id_round'], ),
    sa.PrimaryKeyConstraint('id_student')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('student')
    op.drop_table('option')
    op.drop_table('round')
    op.drop_table('question')
    op.drop_table('station_chrono')
    op.drop_table('shift')
    op.drop_table('group')
    op.drop_table('station')
    op.drop_table('ecoe_chrono')
    op.drop_table('day')
    op.drop_table('area')
    op.drop_table('ecoe')
    op.drop_table('alarm')
    op.drop_table('organization')
    op.drop_table('chronometer')
    # ### end Alembic commands ###
