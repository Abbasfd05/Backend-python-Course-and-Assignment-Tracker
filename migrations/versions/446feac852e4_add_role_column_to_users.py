"""add role column to users

Revision ID: 446feac852e4
Revises: 8a1f3c9d2b4e
Create Date: 2026-10-07 19:06:31.216088

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '446feac852e4'
down_revision: Union[str, Sequence[str], None] = '8a1f3c9d2b4e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('courses', 'description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('courses', 'semester',
               existing_type=sa.VARCHAR(),
               nullable=False)

    user_role = sa.Enum('STUDENT', 'INSTRUCTOR', 'ADMIN', name='user_role')
    user_role.create(op.get_bind(), checkfirst=True)
    op.add_column('users', sa.Column('role', user_role, nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'role')
    sa.Enum(name='user_role').drop(op.get_bind(), checkfirst=True)
    op.alter_column('courses', 'semester',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('courses', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)