import hashlib
import time
import string
import json

def get_rotation_window(rotation_unit):
    now = int(time.time())
    unit_seconds = {
        'second': 1,
        'minute': 60,
        'hour': 3600,
        'day': 86400,
        'week': 604800,
        'month': 2629746
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

    password_chars = required_chars[:]
    i = 8
    while len(password_chars) < length:
        byte = hash_digest[i % len(hash_digest): (i % len(hash_digest)) + 2]
        char = allowed_chars[int(byte, 16) % len(allowed_chars)]
        password_chars.append(char)
        i += 2

    password = ''.join(crypto_deterministic_shuffle(password_chars, base_seed))
    return password

def load_config_and_generate(json_file_path, master_secret):
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    for entry in data.get("services", []):
        identifier = entry["identifier"]
        length = entry.get("length", 16)
        rotation_unit = entry.get("rotation_unit", "month")
        require_uppercase = entry.get("require_uppercase", True)
        require_lowercase = entry.get("require_lowercase", True)
        require_digits = entry.get("require_digits", True)
        require_specials = entry.get("require_specials", True)
        only_digits = entry.get("only_digits", False)

        password = generate_password(
            master_secret=master_secret,
            identifier=identifier,
            rotation_unit=rotation_unit,
            length=length,
            require_uppercase=require_uppercase,
            require_lowercase=require_lowercase,
            require_digits=require_digits,
            require_specials=require_specials,
            only_digits=only_digits,
        )

        print(f"{identifier}: {password}")

if __name__ == "__main__":
    master_secret = input("Enter your master secret: ").strip()
    load_config_and_generate("config.json", master_secret)