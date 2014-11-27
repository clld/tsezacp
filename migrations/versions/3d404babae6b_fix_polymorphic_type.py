"""fix polymorphic_type

Revision ID: 3d404babae6b
Revises: 
Create Date: 2014-11-26 15:42:10.933000

"""

# revision identifiers, used by Alembic.
revision = '3d404babae6b'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    update_pmtype(['contribution', 'sentence', 'unit'], 'base', 'custom')


def downgrade():
    update_pmtype(['contribution', 'sentence', 'unit'], 'custom', 'base')


def update_pmtype(tablenames, before, after):
    for table in tablenames:
        op.execute(sa.text('UPDATE %s SET polymorphic_type = :after '
            'WHERE polymorphic_type = :before' % table
            ).bindparams(before=before, after=after))
