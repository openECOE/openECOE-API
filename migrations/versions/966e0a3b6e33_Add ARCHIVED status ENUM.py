"""Add ARCHIVED status ENUM

Revision ID: 966e0a3b6e33
Revises: 3be7c7f85afa
Create Date: 2020-02-17 13:47:26.077751

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '966e0a3b6e33'
down_revision = '3be7c7f85afa'
branch_labels = None
depends_on = None

old_options = ('DRAFT', 'PUBLISHED')
new_options = sorted(old_options + ('ARCHIVED',))

old_type = sa.Enum(*old_options, name='status')
new_type = sa.Enum(*new_options, name='status')


def upgrade():

    op.alter_column("ecoe", "status", existing_type=old_type, type_=new_type)


def downgrade():
    op.alter_column("ecoe", "status", existing_type=new_type, type_=old_type)