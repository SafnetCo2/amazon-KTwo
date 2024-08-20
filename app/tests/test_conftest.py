import pytest
from app import create_app, db
from app.models import User, Invitation, Store, Product, Inventory, SupplyRequest, Payment


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def init_database():
    user = User(
        user_name='testuser',
        email='test@example.com',
        password_hash='hashed_password',
        role='admin',
        is_active=True,
        confirmed_admin=True
    )
    db.session.add(user)
    db.session.commit()
    return user

# Test cases start here


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b"Welcome to Josys Shop!"


def test_get_users(client, init_database):
    response = client.get('/users')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert len(data['data']) > 0


def test_create_user(client):
    new_user = {
        'user_name': 'newuser',
        'email': 'newuser@example.com',
        'password_hash': 'hashed_password',
        'role': 'user',
        'is_active': True,
        'confirmed_admin': False
    }
    response = client.post('/users', json=new_user)
    assert response.status_code == 201
    data = response.get_json()
    assert data['user_name'] == 'newuser'


def test_get_user(client, init_database):
    user = init_database
    response = client.get(f'/users/{user.user_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['data']['user_name'] == user.user_name


def test_update_user(client, init_database):
    user = init_database
    updated_data = {
        'user_name': 'updateduser'
    }
    response = client.put(f'/users/{user.user_id}', json=updated_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['user_name'] == 'updateduser'


def test_delete_user(client, init_database):
    user = init_database
    response = client.delete(f'/users/{user.user_id}')
    assert response.status_code == 204

# Invitations tests


def test_get_invitations(client):
    response = client.get('/invitations')
    assert response.status_code == 200


def test_create_invitation(client, init_database):
    new_invitation = {
        'email': 'invitee@example.com',
        'expiry_date': '2024-12-31',
        'user_id': init_database.user_id
    }
    response = client.post('/invitations', json=new_invitation)
    assert response.status_code == 201
    data = response.get_json()
    assert data['email'] == 'invitee@example.com'


def test_get_invitation(client, init_database):
    new_invitation = {
        'email': 'invitee@example.com',
        'expiry_date': '2024-12-31',
        'user_id': init_database.user_id
    }
    client.post('/invitations', json=new_invitation)
    response = client.get('/invitations/1')
    assert response.status_code == 200


def test_update_invitation(client):
    updated_data = {
        'email': 'updated@example.com'
    }
    response = client.put('/invitations/1', json=updated_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['email'] == 'updated@example.com'


def test_delete_invitation(client):
    response = client.delete('/invitations/1')
    assert response.status_code == 204

# Store tests


def test_get_stores(client):
    response = client.get('/stores')
    assert response.status_code == 200


def test_create_store(client):
    new_store = {
        'store_name': 'newstore',
        'location': 'New York'
    }
    response = client.post('/stores', json=new_store)
    assert response.status_code == 201
    data = response.get_json()
    assert data['store_name'] == 'newstore'


def test_get_store(client):
    response = client.get('/stores/1')
    assert response.status_code == 200


def test_update_store(client):
    updated_data = {
        'store_name': 'updatedstore'
    }
    response = client.put('/stores/1', json=updated_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['store_name'] == 'updatedstore'


def test_delete_store(client):
    response = client.delete('/stores/1')
    assert response.status_code == 204

# Product tests


def test_get_products(client):
    response = client.get('/products')
    assert response.status_code == 200


def test_create_product(client):
    new_product = {
        'product_name': 'newproduct',
        'buying_price': 100,
        'selling_price': 150
    }
    response = client.post('/products', json=new_product)
    assert response.status_code == 201
    data = response.get_json()
    assert data['product_name'] == 'newproduct'


def test_get_product(client):
    response = client.get('/products/1')
    assert response.status_code == 200


def test_update_product(client):
    updated_data = {
        'product_name': 'updatedproduct'
    }
    response = client.put('/products/1', json=updated_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['product_name'] == 'updatedproduct'


def test_delete_product(client):
    response = client.delete('/products/1')
    assert response.status_code == 204

# Inventory tests


def test_get_inventory(client):
    response = client.get('/inventory')
    assert response.status_code == 200


def test_create_inventory_item(client):
    new_item = {
        'product_id': 1,
        'store_id': 1,
        'quantity_received': 50,
        'quantity_in_stock': 45,
        'quantity_spoilt': 5,
        'payment_status': 'Paid'
    }
    response = client.post('/inventory', json=new_item)
    assert response.status_code == 201
    data = response.get_json()
    assert data['quantity_received'] == 50


def test_get_inventory_item(client):
    response = client.get('/inventory/1')
    assert response.status_code == 200


def test_update_inventory_item(client):
    updated_data = {
        'quantity_received': 60
    }
    response = client.put('/inventory/1', json=updated_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['quantity_received'] == 60


def test_delete_inventory_item(client):
    response = client.delete('/inventory/1')
    assert response.status_code == 204

# Supply Request tests


def test_get_supply_requests(client):
    response = client.get('/supply_requests')
    assert response.status_code == 200


def test_create_supply_request(client):
    new_request = {
        'product_id': 1,
        'store_id': 1,
        'quantity_requested': 100,
        'request_date': '2024-08-01',
        'status': 'Pending'
    }
    response = client.post('/supply_requests', json=new_request)
    assert response.status_code == 201
    data = response.get_json()
    assert data['quantity_requested'] == 100


def test_get_supply_request(client):
    response = client.get('/supply_requests/1')
    assert response.status_code == 200


def test_update_supply_request(client):
    updated_data = {
        'quantity_requested': 120
    }
    response = client.put('/supply_requests/1', json=updated_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['quantity_requested'] == 120


def test_delete_supply_request(client):
    response = client.delete('/supply_requests/1')
    assert response.status_code == 204

# Payments tests


def test_get_payments(client):
    response = client.get('/payments')
    assert response.status_code == 200


def test_create_payment(client):
    new_payment = {
        'amount': 500,
        'payment_date': '2024-08-01',
        'payment_method': 'Credit Card'
    }
    response = client.post('/payments', json=new_payment)
    assert response.status_code == 201
    data = response.get_json()
    assert data['amount'] == 500


def test_get_payment(client):
    response = client.get('/payments/1')
    assert response.status_code == 200


def test_update_payment(client):
    updated_data = {
        'amount': 600
    }
    response = client.put('/payments/1', json=updated_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['amount'] == 600


def test_delete_payment(client):
    response = client.delete('/payments/1')
    assert response.status_code == 204
