"""empty message

Revision ID: 2c82e7e2b65a
Revises: c45fcecdccda
Create Date: 2020-03-14 19:47:03.838832

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c82e7e2b65a'
down_revision = 'c45fcecdccda'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('jobs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('last_done', sa.DateTime(), nullable=True),
    sa.Column('frequency', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_jobs_description'), 'jobs', ['description'], unique=False)
    op.create_index(op.f('ix_jobs_frequency'), 'jobs', ['frequency'], unique=False)
    op.create_index(op.f('ix_jobs_last_done'), 'jobs', ['last_done'], unique=False)
    op.create_index(op.f('ix_jobs_title'), 'jobs', ['title'], unique=True)
    op.drop_index('ix_job_description', table_name='job')
    op.drop_index('ix_job_frequency', table_name='job')
    op.drop_index('ix_job_last_done', table_name='job')
    op.drop_index('ix_job_title', table_name='job')
    op.drop_table('job')
    op.drop_index('ix_location_name', table_name='location')
    op.drop_table('location')
    op.drop_index('ix_user_email', table_name='user')
    op.drop_index('ix_user_username', table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=64), nullable=True),
    sa.Column('email', sa.VARCHAR(length=120), nullable=True),
    sa.Column('password_hash', sa.VARCHAR(length=128), nullable=True),
    sa.Column('_phone_number', sa.VARCHAR(length=255), nullable=True),
    sa.Column('phone_country_code', sa.VARCHAR(length=8), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_user_username', 'user', ['username'], unique=1)
    op.create_index('ix_user_email', 'user', ['email'], unique=1)
    op.create_table('location',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_location_name', 'location', ['name'], unique=1)
    op.create_table('job',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=64), nullable=True),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.Column('last_done', sa.DATETIME(), nullable=True),
    sa.Column('frequency', sa.VARCHAR(length=64), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('location_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['location_id'], ['location.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_job_title', 'job', ['title'], unique=1)
    op.create_index('ix_job_last_done', 'job', ['last_done'], unique=False)
    op.create_index('ix_job_frequency', 'job', ['frequency'], unique=False)
    op.create_index('ix_job_description', 'job', ['description'], unique=False)
    op.drop_index(op.f('ix_jobs_title'), table_name='jobs')
    op.drop_index(op.f('ix_jobs_last_done'), table_name='jobs')
    op.drop_index(op.f('ix_jobs_frequency'), table_name='jobs')
    op.drop_index(op.f('ix_jobs_description'), table_name='jobs')
    op.drop_table('jobs')
    # ### end Alembic commands ###
