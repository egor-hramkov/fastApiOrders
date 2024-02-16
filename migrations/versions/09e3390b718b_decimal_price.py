"""decimal price

Revision ID: 09e3390b718b
Revises: 7691458bd16c
Create Date: 2024-02-15 15:48:08.105061

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '09e3390b718b'
down_revision: Union[str, None] = '7691458bd16c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('items', 'price',
               existing_type=sa.INTEGER(),
               type_=sa.Numeric(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('items', 'price',
               existing_type=sa.Numeric(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    # ### end Alembic commands ###