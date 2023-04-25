"""Creación del campo Description en la tabla ECOE

Revision ID: 7d8e19c8d158
Revises: 6e365ec7cf27
Create Date: 2022-11-14 13:07:37.528000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7d8e19c8d158'
down_revision = '6e365ec7cf27'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ecoe', sa.Column('description', mysql.LONGTEXT(), nullable=True))
    op.alter_column('question', 'question_schema',
               existing_type=mysql.LONGTEXT(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('question', 'question_schema',
               existing_type=mysql.LONGTEXT(),
               nullable=True)
    op.drop_column('ecoe', 'description')
    # ### end Alembic commands ###
