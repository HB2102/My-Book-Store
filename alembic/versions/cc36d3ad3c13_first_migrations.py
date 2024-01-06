"""first migrations

Revision ID: cc36d3ad3c13
Revises: 47da40c14e3d
Create Date: 2024-01-07 01:48:37.549025

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc36d3ad3c13'
down_revision: Union[str, None] = '47da40c14e3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
