"""update geometry column type

Revision ID: update_geometry_column
Revises: update_geometry_type
Create Date: 2024-05-04 07:42:15.299016

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'update_geometry_column'
down_revision: Union[str, None] = 'update_geometry_type'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Update the geometry column type to GEOMETRY
    op.execute('ALTER TABLE cities ALTER COLUMN geometry TYPE geometry(GEOMETRY, 4326)')


def downgrade() -> None:
    """Downgrade schema."""
    # Revert back to POLYGON type
    op.execute('ALTER TABLE cities ALTER COLUMN geometry TYPE geometry(POLYGON, 4326)') 