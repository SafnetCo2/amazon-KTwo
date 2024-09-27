from flask import current_app as app, request, jsonify
from flask_cors import CORS
from app import db
from app.models import User, Invitation, Store, Product, Inventory, SupplyRequest, Payment
import uuid
import bcrypt
# Enable CORS for all routes
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return "Welcome to Josys Shop!"

# User Routes

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_data = [user.to_dict() for user in users]
    return jsonify({
        "status": "success",
        "message": "Users retrieved successfully",
        "data": users_data
    })

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        "status": "success",
        "message": "User retrieved successfully",
        "data": user.to_dict()
    })

# Password hashing function
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    # Check for required fields in the incoming data
    required_fields = ['user_name', 'email', 'password', 'role', 'is_active', 'confirmed_admin']
    for field in required_fields:
        if field not in data:
            return jsonify({"status": "error", "message": f"{field} is required"}), 400

    # Extract and hash the password
    password = data['password']
    password_hash = hash_password(password)

    # Create a new user
    new_user = User(
        user_name=data['user_name'],
        email=data['email'],
        password_hash=password_hash,
        role=data['role'],
        is_active=data['is_active'],
        confirmed_admin=data['confirmed_admin']
    )

    # Save the user to the database
    db.session.add(new_user)
    db.session.commit()
    
    # Prepare the response structure including user_id
    response_data = {
        "user_id": new_user.user_id,
        "confirmed_admin": new_user.confirmed_admin,
        "email": new_user.email,
        "is_active": new_user.is_active,
        "role": new_user.role,
        "user_name": new_user.user_name
    }
    
    return jsonify({"status": "success", "data": response_data}), 201
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.user_name = data.get('user_name', user.user_name)
    user.email = data.get('email', user.email)
    user.password_hash = data.get('password_hash', user.password_hash)
    user.role = data.get('role', user.role)
    user.is_active = data.get('is_active', user.is_active)
    user.confirmed_admin = data.get('confirmed_admin', user.confirmed_admin)
    db.session.commit()
    return jsonify(user.to_dict())

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204

# Invitation Routes

@app.route('/invitations', methods=['GET'])
def get_invitations():
    invitations = Invitation.query.all()
    invitations_data = [invitation.to_dict() for invitation in invitations]
    return jsonify({
        "status": "success",
        "message": "Invitations retrieved successfully",
        "data": invitations_data
    })

@app.route('/invitations/<int:invitation_id>', methods=['GET'])
def get_invitation(invitation_id):
    invitation = Invitation.query.get_or_404(invitation_id)
    return jsonify({
        "status": "success",
        "message": "Invitation retrieved successfully",
        "data": invitation.to_dict()
    })

@app.route('/invitations', methods=['POST'])
def create_invitation():
    data = request.get_json()
    invitation = Invitation(
        token=str(uuid.uuid4()),
        email=data['email'],
        expiry_date=data['expiry_date'],
        user_id=data.get('user_id'),
        is_used=data.get('is_used', False)
    )
    db.session.add(invitation)
    db.session.commit()
    return jsonify(invitation.to_dict()), 201

@app.route('/invitations/<int:invitation_id>', methods=['PUT'])
def update_invitation(invitation_id):
    invitation = Invitation.query.get_or_404(invitation_id)
    data = request.get_json()
    invitation.token = data.get('token', invitation.token)
    invitation.email = data.get('email', invitation.email)
    invitation.expiry_date = data.get('expiry_date', invitation.expiry_date)
    invitation.user_id = data.get('user_id', invitation.user_id)
    invitation.is_used = data.get('is_used', invitation.is_used)
    db.session.commit()
    return jsonify(invitation.to_dict())

@app.route('/invitations/<int:invitation_id>', methods=['DELETE'])
def delete_invitation(invitation_id):
    invitation = Invitation.query.get_or_404(invitation_id)
    db.session.delete(invitation)
    db.session.commit()
    return '', 204

# Store Routes

@app.route('/stores', methods=['GET'])
def get_stores():
    stores = Store.query.all()
    return jsonify([store.to_dict() for store in stores])

@app.route('/stores/<int:store_id>', methods=['GET'])
def get_store(store_id):
    store = Store.query.get_or_404(store_id)
    return jsonify(store.to_dict())

@app.route('/stores', methods=['POST'])
def create_store():
    data = request.get_json()
    store = Store(
        store_name=data['store_name'],
        location=data['location']
    )
    db.session.add(store)
    db.session.commit()
    return jsonify(store.to_dict()), 201

@app.route('/stores/<int:store_id>', methods=['PUT'])
def update_store(store_id):
    store = Store.query.get_or_404(store_id)
    data = request.get_json()
    store.store_name = data.get('store_name', store.store_name)
    store.location = data.get('location', store.location)
    db.session.commit()
    return jsonify(store.to_dict())

@app.route('/stores/<int:store_id>', methods=['DELETE'])
def delete_store(store_id):
    store = Store.query.get_or_404(store_id)
    db.session.delete(store)
    db.session.commit()
    return '', 204

# Product Routes

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    product = Product(
        product_name=data['product_name'],
        buying_price=data['buying_price'],
        selling_price=data['selling_price']
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    product.product_name = data.get('product_name', product.product_name)
    product.buying_price = data.get('buying_price', product.buying_price)
    product.selling_price = data.get('selling_price', product.selling_price)
    db.session.commit()
    return jsonify(product.to_dict())

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return '', 204

# Inventory Routes

@app.route('/inventory', methods=['GET'])
def get_inventory():
    inventory = Inventory.query.all()
    return jsonify([item.to_dict() for item in inventory])

@app.route('/inventory/<int:inventory_id>', methods=['GET'])
def get_inventory_item(inventory_id):
    item = Inventory.query.get_or_404(inventory_id)
    return jsonify(item.to_dict())

@app.route('/inventory', methods=['POST'])
def create_inventory_item():
    data = request.get_json()
    item = Inventory(
        product_id=data['product_id'],
        store_id=data['store_id'],
        quantity_received=data['quantity_received'],
        quantity_in_stock=data['quantity_in_stock'],
        quantity_spoilt=data['quantity_spoilt'],
        payment_status=data['payment_status']
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

@app.route('/inventory/<int:inventory_id>', methods=['PUT'])
def update_inventory_item(inventory_id):
    item = Inventory.query.get_or_404(inventory_id)
    data = request.get_json()
    item.product_id = data.get('product_id', item.product_id)
    item.store_id = data.get('store_id', item.store_id)
    item.quantity_received = data.get('quantity_received', item.quantity_received)
    item.quantity_in_stock = data.get('quantity_in_stock', item.quantity_in_stock)
    item.quantity_spoilt = data.get('quantity_spoilt', item.quantity_spoilt)
    item.payment_status = data.get('payment_status', item.payment_status)
    db.session.commit()
    return jsonify(item.to_dict())

@app.route('/inventory/<int:inventory_id>', methods=['DELETE'])
def delete_inventory_item(inventory_id):
    item = Inventory.query.get_or_404(inventory_id)
    db.session.delete(item)
    db.session.commit()
    return '', 204

# Supply Request Routes

@app.route('/supply_requests', methods=['GET'])
def get_supply_requests():
    requests = SupplyRequest.query.all()
    return jsonify([req.to_dict() for req in requests])

@app.route('/supply_requests/<int:supply_request_id>', methods=['GET'])
def get_supply_request(supply_request_id):
    request = SupplyRequest.query.get_or_404(supply_request_id)
    return jsonify(request.to_dict())

@app.route('/supply_requests', methods=['POST'])
def create_supply_request():
    data = request.get_json()
    request = SupplyRequest(
        product_id=data['product_id'],
        store_id=data['store_id'],
        quantity_requested=data['quantity_requested'],
        request_date=data['request_date'],
        status=data['status']
    )
    db.session.add(request)
    db.session.commit()
    return jsonify(request.to_dict()), 201

@app.route('/supply_requests/<int:supply_request_id>', methods=['PUT'])
def update_supply_request(supply_request_id):
    request = SupplyRequest.query.get_or_404(supply_request_id)
    data = request.get_json()
    request.product_id = data.get('product_id', request.product_id)
    request.store_id = data.get('store_id', request.store_id)
    request.quantity_requested = data.get('quantity_requested', request.quantity_requested)
    request.request_date = data.get('request_date', request.request_date)
    request.status = data.get('status', request.status)
    db.session.commit()
    return jsonify(request.to_dict())

@app.route('/supply_requests/<int:supply_request_id>', methods=['DELETE'])
def delete_supply_request(supply_request_id):
    request = SupplyRequest.query.get_or_404(supply_request_id)
    db.session.delete(request)
    db.session.commit()
    return '', 204

# Payment Routes

@app.route('/payments', methods=['GET'])
def get_payments():
    payments = Payment.query.all()
    return jsonify([payment.to_dict() for payment in payments])

@app.route('/payments/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    return jsonify(payment.to_dict())

@app.route('/payments', methods=['POST'])
def create_payment():
    data = request.get_json()
    payment = Payment(
        amount=data['amount'],
        payment_date=data['payment_date'],
        payment_method=data['payment_method']
    )
    db.session.add(payment)
    db.session.commit()
    return jsonify(payment.to_dict()), 201

@app.route('/payments/<int:payment_id>', methods=['PUT'])
def update_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    data = request.get_json()
    payment.amount = data.get('amount', payment.amount)
    payment.payment_date = data.get('payment_date', payment.payment_date)
    payment.payment_method = data.get('payment_method', payment.payment_method)
    db.session.commit()
    return jsonify(payment.to_dict())

@app.route('/payments/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    db.session.delete(payment)
    db.session.commit()
    return '', 204
