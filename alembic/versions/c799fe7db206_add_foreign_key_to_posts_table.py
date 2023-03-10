"""add foreign key to posts table

Revision ID: c799fe7db206
Revises: aa100f23066e
Create Date: 2023-01-30 18:08:54.598181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c799fe7db206'
down_revision = 'aa100f23066e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id',sa.Integer,nullable=False))
    op.create_foreign_key('posts_users_fk',source_table='posts',referent_table='users',
                        local_cols=['owner_id'],remote_cols=['id'],ondelete='CASCADE')


def downgrade():
    op.drop_constraint('posts_users_fk',table_name='posts')
    op.drop_column('posts','owner_id')
