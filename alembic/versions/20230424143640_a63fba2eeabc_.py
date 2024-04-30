"""empty message

Revision ID: a63fba2eeabc
Revises: 164805dee5bb
Create Date: 2023-04-24 14:36:40.959058

"""

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = "a63fba2eeabc"
down_revision = "164805dee5bb"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("renting", "is_approved", new_column_name="status")


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("renting", "status", new_column_name="is_approved")
    # ### end Alembic commands ###
