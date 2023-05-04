"""first

Revision ID: f206b061c4d6
Revises: 
Create Date: 2023-01-17 12:41:35.406584

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import fastapi_users_db_sqlalchemy
# revision identifiers, used by Alembic.
revision = 'f206b061c4d6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    op.create_table('user',
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('flat',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('cost', sa.BigInteger(), nullable=True),
    sa.Column('user_id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_flat_id'), 'flat', ['id'], unique=True)
    op.create_table('renting',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('lease_range', postgresql.DATERANGE(), nullable=False),
    sa.Column('cost', sa.BigInteger(), nullable=True),
    sa.Column('count_guest', sa.SmallInteger(), nullable=True),
    sa.Column('user_id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=True),
    sa.Column('flat_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['flat_id'], ['flat.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_renting_id'), 'renting', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_renting_id'), table_name='renting')
    op.drop_table('renting')
    op.drop_index(op.f('ix_flat_id'), table_name='flat')
    op.drop_table('flat')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
