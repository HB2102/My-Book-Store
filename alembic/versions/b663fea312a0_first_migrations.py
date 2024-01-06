"""first migrations

Revision ID: b663fea312a0
Revises: 9dcab6f44686
Create Date: 2024-01-07 00:52:53.376257

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b663fea312a0'
down_revision: Union[str, None] = '9dcab6f44686'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
