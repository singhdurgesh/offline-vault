import hashlib
import base64
import datetime
import string
import random

def generate_monthly_password(secret_key, length=12):
    # Get current year and month
    now = datetime.datetime.now()
    month_string = f"{now.year}-{now.month:02d}"

    # Create a unique hash using the month and secret key
    hash_input = (secret_key + month_string).encode('utf-8')
    hash_digest = hashlib.sha256(hash_input).digest()

    # Encode to base64 for more character variety
    base64_encoded = base64.b64encode(hash_digest).decode('utf-8')

    # Allowed characters: alphanumeric + symbols
    allowed_chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"

    # Map hash output to allowed characters
    password = ''.join(allowed_chars[ord(c) % len(allowed_chars)] for c in base64_encoded if c.isalnum())

    return password[:length]

# Example usage
secret = "MySecureSecretKey"
monthly_password = generate_monthly_password(secret, length=16)
print("Monthly Password:", monthly_password)
