"""first migrations

Revision ID: 2309e4f43557
Revises: 704733ea904f
Create Date: 2024-01-07 01:41:04.535001

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2309e4f43557'
down_revision: Union[str, None] = '704733ea904f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
