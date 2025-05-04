"""update geometry type

Revision ID: update_geometry_type
Revises: 
Create Date: 2024-05-03 15:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry

# revision identifiers, used by Alembic.
revision = 'update_geometry_type'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Drop the existing table
    op.drop_table('cities')
    
    # Create the table with the correct geometry type
    op.create_table(
        'cities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('geometry', Geometry(geometry_type='GEOMETRY', srid=4326), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    # Drop the table
    op.drop_table('cities')
    
    # Recreate it with POLYGON type
    op.create_table(
        'cities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('geometry', Geometry(geometry_type='POLYGON', srid=4326), nullable=True),
        sa.PrimaryKeyConstraint('id')
    ) 