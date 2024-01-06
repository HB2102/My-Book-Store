"""first migrations

Revision ID: 435aec8dee68
Revises: 3d12fe9e8968
Create Date: 2024-01-06 16:26:26.986729

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '435aec8dee68'
down_revision: Union[str, None] = '3d12fe9e8968'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
