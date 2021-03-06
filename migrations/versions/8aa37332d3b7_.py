"""empty message

Revision ID: 8aa37332d3b7
Revises: 4c6f3a1626b2
Create Date: 2018-07-14 22:01:38.501053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8aa37332d3b7'
down_revision = '4c6f3a1626b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contact', sa.Column('color', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('contact', 'color')
    # ### end Alembic commands ###
