# BIT4138 - Week 6: Hashing and Password Security

import hashlib
import os
import time

# ── 1. SHA-256 Hashing ────────────────────────────────────────────
def sha256_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

# ── 2. Password Hashing with Salt ─────────────────────────────────
def hash_password(password):
    salt = os.urandom(16).hex()
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return salt, hashed

def verify_password(password, salt, hashed):
    return hashlib.sha256((salt + password).encode()).hexdigest() == hashed

# ── 3. Simple User Database ───────────────────────────────────────
user_db = {}

def register(username, password):
    salt, hashed = hash_password(password)
    user_db[username] = {"salt": salt, "hash": hashed}
    print(f"[Register] User '{username}' registered successfully.")
    print(f"[Register] Salt   : {salt}")
    print(f"[Register] Hash   : {hashed}")

def login(username, password):
    if username not in user_db:
        print(f"[Login] User '{username}' not found.")
        return False
    user = user_db[username]
    if verify_password(password, user["salt"], user["hash"]):
        print(f"[Login] Access granted. Welcome {username}!")
        return True
    else:
        print(f"[Login] Wrong password. Access denied.")
        return False

# ── Main ──────────────────────────────────────────────────────────
print("=" * 50)
print("      Week 6: Hashing and Password Security")
print("=" * 50)

# SHA-256 demo
text = input("\nEnter text to hash: ")
print(f"\n[SHA-256] Input  : {text}")
print(f"[SHA-256] Hash   : {sha256_hash(text)}")

# Show different inputs produce different hashes
print(f"\n[SHA-256] Hash of 'password123' : {sha256_hash('password123')}")
print(f"[SHA-256] Hash of 'password124' : {sha256_hash('password124')}")
print(f"[SHA-256] Hash of 'password123' : {sha256_hash('password123')}")
print("(Notice: same input always produces same hash)")
print("(Notice: one character change produces completely different hash)")

# Registration and Login
print("\n--- User Authentication System ---")
username = input("\nEnter username to register: ")
password = input("Enter password: ")
register(username, password)

# Correct login
print("\n--- Login Attempt 1 (correct password) ---")
login(username, password)

# Wrong login
print("\n--- Login Attempt 2 (wrong password) ---")
login(username, "wrongpassword")

print("\n" + "=" * 50)
