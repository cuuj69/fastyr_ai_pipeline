"""Add user model

Revision ID: 8c4e7e0a1f26
Revises: 3b16488f135c
Create Date: 2024-10-29 22:30:48.272475

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c4e7e0a1f26'
down_revision: Union[str, None] = '3b16488f135c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
