"""init

Revision ID: 6e1abf9c77f4
Revises: 
Create Date: 2026-07-03 09:13:14.832435

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e1abf9c77f4'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('login', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('role', sa.Enum('user', 'admin', name='user_role'), nullable=False, server_default='user'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('login'),
    )

    op.create_table(
        'rooms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('capacity', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )


def downgrade() -> None:
    op.drop_table('rooms')
    op.drop_table('users')
    sa.Enum('user', 'admin', name='user_role').drop(op.get_bind(), if_exists=True)
