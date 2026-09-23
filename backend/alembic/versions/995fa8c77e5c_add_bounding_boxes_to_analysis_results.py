"""add bounding boxes to analysis_results

Revision ID: 995fa8c77e5c
Revises: 768f9edb6026
Create Date: 2026-09-23 16:33:08.337242

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '995fa8c77e5c'
down_revision: Union[str, Sequence[str], None] = '768f9edb6026'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('analysis_results', sa.Column('bounding_boxes', sa.JSON(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('analysis_results', 'bounding_boxes')
