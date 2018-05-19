"""Station order

Revision ID: 0c121185c1fe
Revises: 8051e2b3a2d8
Create Date: 2018-05-19 19:45:30.691145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c121185c1fe'
down_revision = '8051e2b3a2d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('station', sa.Column('order', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('station', 'order')
    # ### end Alembic commands ###