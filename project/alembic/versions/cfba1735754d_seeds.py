"""seeds

Revision ID: cfba1735754d
Revises: bcf1401e4ed6
Create Date: 2024-11-25 12:02:23.613451

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cfba1735754d'
down_revision: Union[str, None] = 'bcf1401e4ed6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""INSERT INTO molecules (id, name) VALUES (0, 'CCO')""")
    op.execute("""INSERT INTO molecules (id, name) VALUES (1, 'c1ccccc1')""")
    op.execute("""INSERT INTO molecules (id, name) VALUES (2, 'CC(=O)O')""")
    op.execute("""INSERT INTO molecules (id, name) VALUES (3, 'CC(=O)Oc1ccccc1C(=O)O')""")


def downgrade() -> None:
    op.execute("TRUNCATE TABLE molecules")
