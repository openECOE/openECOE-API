"""empty message

Revision ID: fe7ca68eea18
Revises: d6fa83f62534
Create Date: 2018-05-30 18:07:44.869220

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fe7ca68eea18'
down_revision = 'd6fa83f62534'
branch_labels = None
depends_on = None


def upgrade():

    op.add_column('station', sa.Column('id_parent_station', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_station_parent'), 'station', ['id_parent_station'])
    op.create_foreign_key('fk_station_station', 'station', 'station', ['id_parent_station'], ['id'])



def downgrade():

    op.drop_constraint('fk_station_station', 'station', type_='foreignkey')
    op.drop_column('station', 'id_parent_station')

