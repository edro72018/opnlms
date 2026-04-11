"""add name fields to users

Revision ID: 50a5b153ae46
Revises: 8c328da1017a
Create Date: 2026-04-05 21:02:48.968720

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50a5b153ae46'
down_revision: Union[str, None] = '8c328da1017a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
