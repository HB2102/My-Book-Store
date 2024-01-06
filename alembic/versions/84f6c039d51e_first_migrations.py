"""first migrations

Revision ID: 84f6c039d51e
Revises: 950a519c8c9d
Create Date: 2024-01-06 16:24:54.447681

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84f6c039d51e'
down_revision: Union[str, None] = '950a519c8c9d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
