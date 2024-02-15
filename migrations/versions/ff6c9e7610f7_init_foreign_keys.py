"""init foreign_keys

Revision ID: ff6c9e7610f7
Revises: 09e3390b718b
Create Date: 2024-02-15 16:20:11.950479

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ff6c9e7610f7'
down_revision: Union[str, None] = '09e3390b718b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orders_items',
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('orders', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'orders', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.drop_column('orders', 'user_id')
    op.drop_table('orders_items')
    # ### end Alembic commands ###
