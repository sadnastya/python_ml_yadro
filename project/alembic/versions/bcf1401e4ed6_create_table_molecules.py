"""create table molecules

Revision ID: bcf1401e4ed6
Revises: 
Create Date: 2024-11-24 18:21:11.350797

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bcf1401e4ed6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('molecules',
                    sa.Column('id', sa.Integer),
                    sa.Column('name', sa.String)
    )


def downgrade() -> None:
    op.drop_table('molecules')
