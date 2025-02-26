
from alembic import op
import sqlalchemy as sa

revision = 'remove_industry_policies'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Drop the industry_policies column
    op.drop_column('enterprises', 'industry_policies')

def downgrade():
    # Add back the industry_policies column
    op.add_column('enterprises', sa.Column('industry_policies', sa.Text(), nullable=True))
