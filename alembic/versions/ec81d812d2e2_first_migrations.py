"""first migrations

Revision ID: ec81d812d2e2
Revises: cf7908367390
Create Date: 2024-01-07 00:55:56.406595

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec81d812d2e2'
down_revision: Union[str, None] = 'cf7908367390'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
