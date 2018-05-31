"""Countdown event and new uk schedule

Revision ID: d6fa83f62534
Revises: bb4fc44a6102
Create Date: 2018-05-30 06:56:52.584543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd6fa83f62534'
down_revision = 'bb4fc44a6102'
branch_labels = None
depends_on = None


def upgrade():

    try:
        op.drop_constraint('schedule_ibfk_1', table_name='schedule', type_='foreignkey')
    except:
        pass

    try:
        op.drop_constraint('schedule_ibfk_3', table_name='schedule', type_='foreignkey')
    except:
        pass

    op.drop_constraint('ecoe_stage_uk', 'schedule', type_='unique')
    op.drop_constraint('station_stage_uk', 'schedule', type_='unique')

    op.create_unique_constraint('ecoe_stage_station_uk', 'schedule', ['id_ecoe', 'id_stage', 'id_station'])
    op.create_index('id_station', 'schedule', ['id_station'])

    try:
        op.create_foreign_key("schedule_ibfk_1", "schedule", "ecoe", ["id_ecoe"], ["id"])
    except:
        pass

    try:
        op.create_foreign_key("schedule_ibfk_3", "schedule", "station", ["id_station"], ["id"])
    except:
        pass

    op.add_column('event', sa.Column('is_countdown', sa.Boolean(), nullable=False))


def downgrade():

    op.create_index('station_stage_uk', 'schedule', ['id_station', 'id_stage'], unique=True)
    op.create_index('ecoe_stage_uk', 'schedule', ['id_ecoe', 'id_stage'], unique=True)

    op.drop_constraint('ecoe_stage_station_uk', 'schedule', type_='unique')
    op.drop_index('id_station', table_name='schedule')

    op.drop_column('event', 'is_countdown')
