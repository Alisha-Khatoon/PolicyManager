"""add reset token fields

Revision ID: 001
Revises: 
Create Date: 2025-02-25

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('users', sa.Column('reset_token', sa.String(255), unique=True))
    op.add_column('users', sa.Column('reset_token_expiry', sa.DateTime))

def downgrade():
    op.drop_column('users', 'reset_token_expiry')
    op.drop_column('users', 'reset_token')
