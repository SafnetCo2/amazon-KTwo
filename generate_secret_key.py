import secrets

# Generate a random secret key
secret_key = secrets.token_hex(16)  # 32 characters long hex string
print(secret_key)
