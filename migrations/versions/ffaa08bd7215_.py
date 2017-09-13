"""empty message

Revision ID: ffaa08bd7215
Revises: 
Create Date: 2017-09-14 00:40:29.521949

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ffaa08bd7215'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=20), nullable=True),
    sa.Column('last_name', sa.String(length=20), nullable=True),
    sa.Column('username', sa.String(length=30), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password', sa.String(length=120), nullable=True),
    sa.Column('ip_address', sa.String(length=24), nullable=True),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('shops',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('shop_name', sa.String(length=120), nullable=True),
    sa.Column('shop_type', sa.String(length=15), nullable=False),
    sa.Column('shop_category', sa.String(length=30), nullable=False),
    sa.Column('country', sa.String(length=30), nullable=True),
    sa.Column('county', sa.String(length=30), nullable=True),
    sa.Column('town_city', sa.String(length=30), nullable=True),
    sa.Column('physical_address', sa.String(length=100), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_updated', sa.DateTime(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('shop_name')
    )
    op.create_table('items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_name', sa.String(length=120), nullable=True),
    sa.Column('item_price', sa.String(length=15), nullable=False),
    sa.Column('item_description', sa.String(length=120), nullable=False),
    sa.Column('item_category', sa.String(length=20), nullable=False),
    sa.Column('item_subcategory', sa.String(length=20), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('shop_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['shop_id'], ['shops.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('item_name')
    )
    op.create_table('services',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('service_name', sa.String(length=120), nullable=True),
    sa.Column('service_price', sa.String(length=15), nullable=False),
    sa.Column('service_description', sa.String(length=120), nullable=False),
    sa.Column('service_category', sa.String(length=20), nullable=False),
    sa.Column('service_subcategory', sa.String(length=20), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('shop_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['shop_id'], ['shops.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('service_name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('services')
    op.drop_table('items')
    op.drop_table('shops')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###