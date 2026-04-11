"""add sex field to users

Revision ID: c1a3f2e8d90b
Revises: b85a2ebd5164
Create Date: 2026-04-09 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1a3f2e8d90b'
down_revision: Union[str, None] = 'b85a2ebd5164'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column(
        'sex',
        sa.Enum('masculino', 'femenino', name='usersex', native_enum=False),
        nullable=True,
    ))


def downgrade() -> None:
    op.drop_column('users', 'sex')
