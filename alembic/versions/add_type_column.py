"""add type column

Revision ID: add_type_column
Revises: update_geometry_column
Create Date: 2024-05-04 07:52:15.299016

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'add_type_column'
down_revision: Union[str, None] = 'update_geometry_column'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add the type column
    op.add_column('cities', sa.Column('type', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove the type column
    op.drop_column('cities', 'type') 