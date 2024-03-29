"""Inclusión ID del job asociado a la generación de Reportes a la tabla ECOE

Revision ID: d724f6ade78a
Revises: 7d8e19c8d158
Create Date: 2022-11-23 14:15:08.547471

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd724f6ade78a'
down_revision = '7d8e19c8d158'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ecoe', sa.Column('id_job_reports', sa.String(length=36), nullable=True))
    op.create_foreign_key('fk_job_reports_ecoe', 'ecoe', 'job', ['id_job_reports'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_job_reports_ecoe', 'ecoe', type_='foreignkey')
    op.drop_column('ecoe', 'id_job_reports')
    # ### end Alembic commands ###
