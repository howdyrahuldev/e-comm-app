"""Create users table

Revision ID: 180006e4e7e5
Revises: 800e89a7dc4a
Create Date: 2024-10-25 02:26:46.295734

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '180006e4e7e5'
down_revision: Union[str, None] = '800e89a7dc4a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('Users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('username', sa.Text(), nullable=False),
    sa.Column('email', sa.Text(), nullable=False),
    sa.Column('hashed_password', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )


def downgrade() -> None:
    op.drop_table('Users')
