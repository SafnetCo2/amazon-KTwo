"""Recreate migration after missing revision

Revision ID: 4a952f580e91
Revises: 
Create Date: 2024-08-06 19:24:15.400437
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4a952f580e91'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Drop foreign key constraints first
    op.drop_constraint('invitations_user_id_fkey', 'invitations', type_='foreignkey')
    op.drop_constraint('supply_requests_user_id_fkey', 'supply_requests', type_='foreignkey')
    op.drop_constraint('supply_requests_inventory_id_fkey', 'supply_requests', type_='foreignkey')
    op.drop_constraint('inventory_store_id_fkey', 'inventory', type_='foreignkey')
    
    # Drop tables
    op.drop_table('supply_requests')
    op.drop_table('users')
    op.drop_table('invitations')
    op.drop_table('stores')
    op.drop_table('inventory')
    op.drop_table('payments')

def downgrade():
    # Recreate tables
    op.create_table('payments',
        sa.Column('payment_id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('supplier_name', sa.VARCHAR(length=25), autoincrement=False, nullable=False),
        sa.Column('invoice_number', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
        sa.Column('amount', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
        sa.Column('payment_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
        sa.Column('payment_status', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint('payment_id', name='payments_pkey')
    )
    op.create_table('inventory',
        sa.Column('inventory_id', sa.INTEGER(), server_default=sa.text("nextval('inventory_inventory_id_seq'::regclass)"), autoincrement=True, nullable=False),
        sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('store_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('quantity_received', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('quantity_in_stock', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('quantity_spoilt', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('payment_status', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['store_id'], ['stores.store_id'], name='inventory_store_id_fkey'),
        sa.PrimaryKeyConstraint('inventory_id', name='inventory_pkey'),
        postgresql_ignore_search_path=False
    )
    op.create_table('stores',
        sa.Column('store_id', sa.INTEGER(), server_default=sa.text("nextval('stores_store_id_seq'::regclass)"), autoincrement=True, nullable=False),
        sa.Column('store_name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
        sa.Column('location', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint('store_id', name='stores_pkey'),
        postgresql_ignore_search_path=False
    )
    op.create_table('invitations',
        sa.Column('invitation_id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('token', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
        sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
        sa.Column('expiry_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
        sa.Column('is_used', sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='invitations_user_id_fkey'),
        sa.PrimaryKeyConstraint('invitation_id', name='invitations_pkey'),
        sa.UniqueConstraint('token', name='invitations_token_key')
    )
    op.create_table('users',
        sa.Column('user_id', sa.INTEGER(), server_default=sa.text("nextval('users_user_id_seq'::regclass)"), autoincrement=True, nullable=False),
        sa.Column('user_name', sa.VARCHAR(length=25), autoincrement=False, nullable=False),
        sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
        sa.Column('password_hash', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
        sa.Column('role', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
        sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.Column('confirmed_admin', sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint('user_id', name='users_pkey'),
        sa.UniqueConstraint('email', name='users_email_key'),
        postgresql_ignore_search_path=False
    )
    op.create_table('supply_requests',
        sa.Column('request_id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('inventory_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('request_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
        sa.Column('status', sa.VARCHAR(length=10), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['inventory_id'], ['inventory.inventory_id'], name='supply_requests_inventory_id_fkey'),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='supply_requests_user_id_fkey'),
        sa.PrimaryKeyConstraint('request_id', name='supply_requests_pkey')
    )
