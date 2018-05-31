"""Merge revisions 332bcb12723c, be3a27c5c76b

Revision ID: bb4fc44a6102
Revises: 332bcb12723c, be3a27c5c76b
Create Date: 2018-05-30 12:23:20.480222

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb4fc44a6102'
down_revision = ('332bcb12723c', 'be3a27c5c76b')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
