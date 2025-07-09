import hashlib
import time
import string

# time.time() always returns Unix time – the number of whole-and-fractional seconds
# that have elapsed since 00:00:00 UTC on 1 January 1970 (the Unix epoch).
def get_rotation_window(rotation_unit):
    now = int(time.time())
    unit_seconds = {
        'second': 1,
        'minute': 60,
        'hour': 3600,
        'day': 86400,
        'week': 604800,
        'month': 2629746  # ≈ 30.44 days
    }
    return now // unit_seconds.get(rotation_unit, 2629746)

def crypto_deterministic_shuffle(items, seed):
    hashed = [(c, hashlib.sha256(f"{seed}:{i}".encode()).hexdigest()) for i, c in enumerate(items)]
    hashed.sort(key=lambda x: x[1])
    return [c for c, _ in hashed]

def generate_password(
    master_secret,
    identifier,
    rotation_unit="month",
    length=16,
    require_uppercase=True,
    require_lowercase=True,
    require_digits=True,
    require_specials=True,
    only_digits=False,
):
    if length < 4:
        raise ValueError("Password length must be at least 4 for secure constraints")

    rotation_window = get_rotation_window(rotation_unit)
    base_seed = f"{master_secret}:{identifier}:{rotation_window}"
    hash_digest = hashlib.sha256(base_seed.encode()).hexdigest()

    # Define character pools
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    specials = "!@#$%^&*()-_=+"

    required_chars = []

    if only_digits:
        allowed_chars = digits
    else:
        allowed_chars = ''
        if require_lowercase:
            allowed_chars += lowercase
            required_chars.append(lowercase[int(hash_digest[0:2], 16) % len(lowercase)])
        if require_uppercase:
            allowed_chars += uppercase
            required_chars.append(uppercase[int(hash_digest[2:4], 16) % len(uppercase)])
        if require_digits:
            allowed_chars += digits
            required_chars.append(digits[int(hash_digest[4:6], 16) % len(digits)])
        if require_specials:
            allowed_chars += specials
            required_chars.append(specials[int(hash_digest[6:8], 16) % len(specials)])

    # Generate rest of the characters deterministically
    password_chars = required_chars[:]
    i = 8
    while len(password_chars) < length:
        byte = hash_digest[i % len(hash_digest): (i % len(hash_digest)) + 2]
        char = allowed_chars[int(byte, 16) % len(allowed_chars)]
        password_chars.append(char)
        i += 2

    # Deterministic crypto shuffle
    password = ''.join(crypto_deterministic_shuffle(password_chars, base_seed))
    return password

# Example usage
pwd = generate_password(
    master_secret="UltraSecret",
    identifier="github.com",
    rotation_unit="month",
    length=16,
    require_uppercase=True,
    require_lowercase=True,
    require_digits=True,
    require_specials=True,
    only_digits=False
)

print("Generated Password:", pwd)

pwd2 = generate_password(
    master_secret="HDFCBankOTP",
    identifier="hdfccard",
    rotation_unit="year",
    length=4,
    require_uppercase=True,
    require_lowercase=True,
    require_digits=True,
    require_specials=True,
    only_digits=True
)

pwd2 = generate_password(
    master_secret="HDFCBankOTP",
    identifier="hdfccard",
    rotation_unit="second",
    length=4,
    require_uppercase=True,
    require_lowercase=True,
    require_digits=True,
    require_specials=True,
    only_digits=True
)

print("Generated OTP:", pwd2)

pwd3 = generate_password(
    master_secret="HDFCBankOTP",
    identifier="hdfccard",
    rotation_unit="month",
    length=64,
    require_uppercase=True,
    require_lowercase=True,
    require_digits=True,
    require_specials=True,
    only_digits=False
)

print("Generated Long Password:", pwd3)

