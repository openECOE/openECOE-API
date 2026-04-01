"""add user language column

Revision ID: a9f3c1b2d4e5
Revises: 259c2b26d274
Create Date: 2026-01-22 16:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a9f3c1b2d4e5'
down_revision = '259c2b26d274'
branch_labels = None
depends_on = None


def upgrade():
    # create enum type if not exists and add column with default
    language_enum = sa.Enum('es', 'en', 'va', name='language_types')
    language_enum.create(op.get_bind(), checkfirst=True)
    op.add_column('user', sa.Column('language', language_enum, nullable=False, server_default='es'))


def downgrade():
    # remove column and drop enum type
    op.drop_column('user', 'language')
    language_enum = sa.Enum('es', 'en', 'va', name='language_types')
    language_enum.drop(op.get_bind(), checkfirst=True)
