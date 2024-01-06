"""first migrations

Revision ID: 67a4f5c693e1
Revises: 2309e4f43557
Create Date: 2024-01-07 01:44:42.999950

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67a4f5c693e1'
down_revision: Union[str, None] = '2309e4f43557'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
