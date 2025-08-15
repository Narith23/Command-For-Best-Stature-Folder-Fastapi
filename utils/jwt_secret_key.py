import secrets


# Generate a 256-bit (32-byte) secret key
def generate_secret_key():
    # Generate a 256-bit (32-byte) secret key
    JWT_SECRET_KEY = secrets.token_hex(32)
    return JWT_SECRET_KEY
