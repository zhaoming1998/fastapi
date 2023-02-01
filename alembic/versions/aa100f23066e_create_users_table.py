"""create users table

Revision ID: aa100f23066e
Revises: 0712f1d510e9
Create Date: 2023-01-30 17:48:17.038166

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa100f23066e'
down_revision = '0712f1d510e9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id',sa.Integer,primary_key=True,nullable=False),
                    sa.Column('email',sa.String,nullable=False,unique=True),
                    sa.Column('password',sa.String,nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,
                                server_default=sa.text('NOW()')))


def downgrade():
    op.drop_table('users')
