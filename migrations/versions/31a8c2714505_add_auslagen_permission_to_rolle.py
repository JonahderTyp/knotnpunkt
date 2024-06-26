"""Add Auslagen permission to Rolle

Revision ID: 31a8c2714505
Revises: 25402355d8fd
Create Date: 2023-04-05 21:54:37.348731

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31a8c2714505'
down_revision = '25402355d8fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Rolle', sa.Column('lesenAlleAuslagen', sa.Boolean(), nullable=True))
    op.add_column('Rolle', sa.Column('freigebenAuslagen', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Rolle', 'freigebenAuslagen')
    op.drop_column('Rolle', 'lesenAlleAuslagen')
    # ### end Alembic commands ###
