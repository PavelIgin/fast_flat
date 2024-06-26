"""add column in flat

Revision ID: 164805dee5bb
Revises: b1f8ff7cddc0
Create Date: 2023-04-18 14:49:31.132322

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "164805dee5bb"
down_revision = "b1f8ff7cddc0"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("flat", sa.Column("address", sa.String(), nullable=True))
    op.add_column("flat", sa.Column("floor", sa.Integer(), nullable=True))
    op.add_column("flat", sa.Column("quadrature", sa.Integer(), nullable=True))
    op.add_column(
        "user", sa.Column("telegram_contact", sa.String(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "telegram_contact")
    op.drop_column("flat", "quadrature")
    op.drop_column("flat", "floor")
    op.drop_column("flat", "address")
    # ### end Alembic commands ###
