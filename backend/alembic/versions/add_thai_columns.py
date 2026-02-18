"""initial tables

Revision ID: b3b72141a976
Revises: 
Create Date: 2025-12-21 16:57:47.652787

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = 'b3b72141a976'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _table_exists(table_name: str) -> bool:
    """Check if a table already exists in the database."""
    bind = op.get_bind()
    insp = inspect(bind)
    return table_name in insp.get_table_names()


def _index_exists(index_name: str, table_name: str) -> bool:
    """Check if an index already exists on a table."""
    bind = op.get_bind()
    insp = inspect(bind)
    indexes = insp.get_indexes(table_name)
    return any(idx['name'] == index_name for idx in indexes)


def upgrade() -> None:
    """Upgrade schema."""
    # Create execution_history only if it doesn't exist
    if not _table_exists('execution_history'):
        op.create_table('execution_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('ticker', sa.String(), nullable=True),
        sa.Column('analysis_date', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
        )

    if _table_exists('execution_history'):
        if not _index_exists('ix_execution_history_id', 'execution_history'):
            op.create_index(op.f('ix_execution_history_id'), 'execution_history', ['id'], unique=False)
        if not _index_exists('ix_execution_history_ticker', 'execution_history'):
            op.create_index(op.f('ix_execution_history_ticker'), 'execution_history', ['ticker'], unique=False)

    # Create report_results only if it doesn't exist
    if not _table_exists('report_results'):
        op.create_table('report_results',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('execution_id', sa.Integer(), nullable=True),
        sa.Column('report_type', sa.String(), nullable=True),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('content', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['execution_id'], ['execution_history.id'], ),
        sa.PrimaryKeyConstraint('id')
        )

    if _table_exists('report_results'):
        if not _index_exists('ix_report_results_id', 'report_results'):
            op.create_index(op.f('ix_report_results_id'), 'report_results', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    if _table_exists('report_results'):
        op.drop_index(op.f('ix_report_results_id'), table_name='report_results')
        op.drop_table('report_results')
    if _table_exists('execution_history'):
        op.drop_index(op.f('ix_execution_history_ticker'), table_name='execution_history')
        op.drop_index(op.f('ix_execution_history_id'), table_name='execution_history')
        op.drop_table('execution_history')