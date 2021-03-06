"""Added code_area

Revision ID: be3a27c5c76b
Revises: aca54da4f713
Create Date: 2018-05-28 09:52:35.646537

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be3a27c5c76b'
down_revision = 'aca54da4f713'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('area', sa.Column('code', sa.String(length=20), nullable=False))

    op.execute(
        'update area set code=id'
    )

    op.create_unique_constraint('code_area_uk', 'area', ['code', 'id_ecoe'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('code_area_uk', 'area', type_='unique')
    op.drop_column('area', 'code')
    # ### end Alembic commands ###
