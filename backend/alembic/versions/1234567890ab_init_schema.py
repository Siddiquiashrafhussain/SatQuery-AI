"""init schema

Revision ID: 1234567890ab
Revises: 
Create Date: 2026-09-23 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import geoalchemy2

# revision identifiers, used by Alembic.
revision: str = '1234567890ab'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enable PostGIS extension
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
    
    # Create users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    # Create scenes
    op.create_table(
        'scenes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('filename', sa.String(), nullable=False),
        sa.Column('storage_path', sa.String(), nullable=False),
        sa.Column('crs', sa.String(), nullable=True),
        sa.Column('bounds', geoalchemy2.types.Geometry(geometry_type='POLYGON', srid=4326, from_text='ST_GeomFromEWKT', name='geometry'), nullable=True),
        sa.Column('bands', sa.Integer(), nullable=True),
        sa.Column('resolution', sa.Float(), nullable=True),
        sa.Column('uploaded_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scenes_id'), 'scenes', ['id'], unique=False)

    # Create queries
    op.create_table(
        'queries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('scene_id', sa.Integer(), nullable=True),
        sa.Column('query_text', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['scene_id'], ['scenes.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_queries_id'), 'queries', ['id'], unique=False)

    # Create analysis_results
    op.create_table(
        'analysis_results',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('query_id', sa.Integer(), nullable=True),
        sa.Column('result_text', sa.String(), nullable=False),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('mask_path', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['query_id'], ['queries.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_analysis_results_id'), 'analysis_results', ['id'], unique=False)

    # Enable RLS on all tables
    op.execute("ALTER TABLE users ENABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE scenes ENABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE queries ENABLE ROW LEVEL SECURITY;")
    op.execute("ALTER TABLE analysis_results ENABLE ROW LEVEL SECURITY;")


def downgrade() -> None:
    op.drop_index(op.f('ix_analysis_results_id'), table_name='analysis_results')
    op.drop_table('analysis_results')
    op.drop_index(op.f('ix_queries_id'), table_name='queries')
    op.drop_table('queries')
    op.drop_index(op.f('ix_scenes_id'), table_name='scenes')
    op.drop_table('scenes')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
