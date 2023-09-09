"""add user table

Revision ID: 97d7cc51c4f6
Revises: 024f2a076650
Create Date: 2023-09-08 06:40:12.173151

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97d7cc51c4f6'
down_revision: Union[str, None] = '024f2a076650'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
