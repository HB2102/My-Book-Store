"""first migrations

Revision ID: a48b8dc851fd
Revises: 435aec8dee68
Create Date: 2024-01-06 16:32:42.578664

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a48b8dc851fd'
down_revision: Union[str, None] = '435aec8dee68'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
