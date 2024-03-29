"""initial migrations

Revision ID: 47da40c14e3d
Revises: ac9ac924a60c
Create Date: 2024-01-07 01:48:24.573154

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '47da40c14e3d'
down_revision: Union[str, None] = 'ac9ac924a60c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'category', ['category_id'], ['id'])

    with op.batch_alter_table('cart', schema=None) as batch_op:
        batch_op.drop_column('number_of_items')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['username'])
        batch_op.drop_column('phone_number')

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('phone_number', sa.VARCHAR(length=20), nullable=True))
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('cart', schema=None) as batch_op:
        batch_op.add_column(sa.Column('number_of_items', sa.INTEGER(), nullable=True))

    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('category_id')

    # ### end Alembic commands ###
