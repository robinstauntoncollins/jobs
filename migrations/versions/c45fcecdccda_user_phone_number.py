"""user phone number

Revision ID: c45fcecdccda
Revises: a863dad41325
Create Date: 2020-03-09 22:18:42.793316

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c45fcecdccda'
down_revision = 'a863dad41325'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('_phone_number', sa.Unicode(length=255), nullable=True))
    op.add_column('user', sa.Column('phone_country_code', sa.Unicode(length=8), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'phone_country_code')
    op.drop_column('user', '_phone_number')
    # ### end Alembic commands ###