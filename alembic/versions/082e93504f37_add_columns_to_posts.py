"""add columns to posts

Revision ID: 082e93504f37
Revises: c799fe7db206
Create Date: 2023-01-30 18:40:37.446591

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '082e93504f37'
down_revision = 'c799fe7db206'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String,nullable=False))
    op.add_column('posts',sa.Column('published',sa.Boolean,nullable=False,server_default='TRUE'))
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,
                                    server_default=sa.text('NOW()')))


def downgrade():
    op.drop_column('posts','content')
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
