"""Add report_template table

Revision ID: 2feeb2157394
Revises: 9b6e8b64a582
Create Date: 2024-06-06 10:32:42.926360

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2feeb2157394'
down_revision = '9b6e8b64a582'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('report_template',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('html', sa.Text(), nullable=True),
    sa.Column('id_ecoe', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_ecoe'], ['ecoe.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('report_template')
    # ### end Alembic commands ###
