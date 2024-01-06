"""first migrations

Revision ID: 950a519c8c9d
Revises: 85bf1ad4395c
Create Date: 2024-01-06 16:14:32.074736

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '950a519c8c9d'
down_revision: Union[str, None] = '85bf1ad4395c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
