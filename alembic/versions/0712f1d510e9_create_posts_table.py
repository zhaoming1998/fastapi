"""create posts table

Revision ID: 0712f1d510e9
Revises: 
Create Date: 2023-01-30 14:50:13.833710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0712f1d510e9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',sa.Column('id',sa.Integer,nullable=False,primary_key=True),
                            sa.Column('title',sa.String,nullable=False))


def downgrade():
    op.drop_table('posts')
