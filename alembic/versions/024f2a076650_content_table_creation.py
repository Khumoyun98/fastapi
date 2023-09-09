"""content table creation

Revision ID: 024f2a076650
Revises: eee4c71c4670
Create Date: 2023-09-08 06:26:10.025491

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '024f2a076650'
down_revision: Union[str, None] = 'eee4c71c4670'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", 'content')
    pass
