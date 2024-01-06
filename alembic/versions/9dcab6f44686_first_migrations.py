"""first migrations

Revision ID: 9dcab6f44686
Revises: 1e449b2d2114
Create Date: 2024-01-06 23:09:31.101698

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9dcab6f44686'
down_revision: Union[str, None] = '1e449b2d2114'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
