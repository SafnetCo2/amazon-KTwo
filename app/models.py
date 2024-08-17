from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(25))
    email = db.Column(db.String(255))
    password_hash = db.Column(db.String(150))
    role = db.Column(db.String(10))
    is_active = db.Column(db.Boolean, default=True)
    confirmed_admin = db.Column(db.Boolean, default=False)  # Update type here


    invitations = db.relationship('Invitation', backref='user', lazy=True)
    supply_requests = db.relationship('SupplyRequest', backref='user', lazy=True)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "email": self.email,
            "role": self.role,
            "is_active": self.is_active,
            "confirmed_admin": self.confirmed_admin
        }

class Invitation(db.Model):
    __tablename__ = 'invitations'
    invitation_id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expiry_date = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)

    def to_dict(self):
        return {
            "invitation_id": self.invitation_id,
            "token": self.token,
            "email": self.email,
            "created_at": self.created_at,
            "expiry_date": self.expiry_date,
            "is_used": self.is_used
        }

class Store(db.Model):
    __tablename__ = 'stores'
    store_id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)

    inventories = db.relationship('Inventory', backref='store', lazy=True)

    def to_dict(self):
        return {
            "store_id": self.store_id,
            "store_name": self.store_name,
            "location": self.location
        }

class Product(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(25), nullable=False)
    buying_price = db.Column(db.String(10), nullable=False)
    selling_price = db.Column(db.String(10), nullable=False)

    inventories = db.relationship('Inventory', backref='product', lazy=True)

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "buying_price": self.buying_price,
            "selling_price": self.selling_price
        }

class Inventory(db.Model):
    __tablename__ = 'inventory'
    inventory_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.store_id'), nullable=False)
    quantity_received = db.Column(db.Integer, nullable=False)
    quantity_in_stock = db.Column(db.Integer, nullable=False)
    quantity_spoilt = db.Column(db.Integer, nullable=False)
    payment_status = db.Column(db.String(10), nullable=False)

    supply_requests = db.relationship('SupplyRequest', backref='inventory', lazy=True)

    def to_dict(self):
        return {
            "inventory_id": self.inventory_id,
            "product_id": self.product_id,
            "store_id": self.store_id,
            "quantity_received": self.quantity_received,
            "quantity_in_stock": self.quantity_in_stock,
            "quantity_spoilt": self.quantity_spoilt,
            "payment_status": self.payment_status
        }

class SupplyRequest(db.Model):
    __tablename__ = 'supply_requests'
    request_id = db.Column(db.Integer, primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.inventory_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(10), nullable=False)

    def to_dict(self):
        return {
            "request_id": self.request_id,
            "inventory_id": self.inventory_id,
            "user_id": self.user_id,
            "request_date": self.request_date,
            "status": self.status
        }

class Payment(db.Model):
    __tablename__ = 'payments'
    payment_id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(25))
    invoice_number = db.Column(db.String(50))
    amount = db.Column(db.String(150))
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    payment_status = db.Column(db.String(10))  # Update length here

    def to_dict(self):
        return {
            "payment_id": self.payment_id,
            "supplier_name": self.supplier_name,
            "invoice_number": self.invoice_number,
            "amount": self.amount,
            "payment_date": self.payment_date,
            "payment_status": self.payment_status
        }
