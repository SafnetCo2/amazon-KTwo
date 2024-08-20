from app import create_app, db
from app.models import User, Invitation, Store, Product, Inventory, SupplyRequest, Payment
from datetime import datetime, timedelta
import os
import uuid
os.environ['DATABASE_URL'] = 'postgresql://josephine:root@localhost/shop_db'


def seed_users():
    users = [
        User(
            user_name='admin',
            email='admin@example.com',
            password_hash='hashed_password1',
            role='superuser',
            confirmed_admin=True),
        User(
            user_name='clerk',
            email='clerk@example.com',
            password_hash='hashed_password2',
            role='clerk',
            confirmed_admin=False)]
    db.session.add_all(users)
    db.session.commit()


def seed_invitations():
    invitations = [
        Invitation(
            token=str(uuid.uuid4()),
            email='admin_invite@example.com',
            created_at=datetime.now(),
            expiry_date=datetime.now() + timedelta(days=7),
            is_used=False,
            user_id=None
        ),
        Invitation(
            token=str(uuid.uuid4()),
            email='clerk_invite@example.com',
            created_at=datetime.now(),
            expiry_date=datetime.now() + timedelta(days=7),
            is_used=False,
            user_id=None
        )
    ]
    db.session.add_all(invitations)
    db.session.commit()


def seed_stores():
    stores = [
        Store(store_name='Main Warehouse', location='Nairobi'),
        Store(store_name='Secondary Warehouse', location='Mombasa')
    ]
    db.session.add_all(stores)
    db.session.commit()


def seed_products():
    products = [
        Product(product_name='Product1', buying_price=100, selling_price=150),
        Product(product_name='Product2', buying_price=200, selling_price=300)
    ]
    db.session.add_all(products)
    db.session.commit()


def seed_inventory():
    inventory_items = [
        Inventory(
            product_id=1,
            store_id=1,
            quantity_received=100,
            quantity_in_stock=100,
            quantity_spoilt=0,
            payment_status='paid'),
        Inventory(
            product_id=2,
            store_id=2,
            quantity_received=200,
            quantity_in_stock=180,
            quantity_spoilt=20,
            payment_status='not paid')]
    db.session.add_all(inventory_items)
    db.session.commit()


def seed_supply_requests():
    supply_requests = [
        SupplyRequest(inventory_id=1, user_id=2, status='pending'),
        SupplyRequest(inventory_id=2, user_id=2, status='approved')
    ]
    db.session.add_all(supply_requests)
    db.session.commit()


def seed_payments():
    payments = [{'supplier_name': 'Supplier1',
                 'invoice_number': 'INV001',
                 'amount': 1500,
                 'payment_date': datetime.now(),
                 'payment_status': 'paid'},
                {'supplier_name': 'Supplier2',
                 'invoice_number': 'INV002',
                 'amount': 3000,
                 'payment_date': datetime.now(),
                 'payment_status': 'not paid'}]

    db.session.bulk_insert_mappings(Payment, payments)
    db.session.commit()


def main():
    app = create_app()  # Create the Flask application instance
    with app.app_context():
        db.create_all()  # Create database tables
        seed_users()
        seed_invitations()
        seed_stores()
        seed_products()
        seed_inventory()
        seed_supply_requests()
        seed_payments()


if __name__ == "__main__":
    main()
