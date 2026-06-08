# BIT4138 - Creative Task: Secure Student Report Submission System
# Covers: Week 2 (Caesar), Week 3 (RC4), Week 4 (AES), Week 5 (RSA), Week 6 (Hashing)

import hashlib
import os
import json
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# ── Week 2: Caesar Cipher (encode filename) ───────────────────────
def caesar_encrypt(text, shift=4):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def caesar_decrypt(text, shift=4):
    return caesar_encrypt(text, -shift)

# ── Week 3: RC4 (encrypt metadata) ───────────────────────────────
def rc4(key, text):
    key = [ord(c) for c in key]
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    result = []
    for char in text:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        result.append(chr(ord(char) ^ S[(S[i] + S[j]) % 256]))
    return ''.join(result)

# ── Week 4: AES (encrypt report content) ─────────────────────────
def aes_encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return cipher.iv, ciphertext

def aes_decrypt(iv, ciphertext, key):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size).decode()

# ── Week 5: RSA (protect AES key) ────────────────────────────────
def rsa_encrypt_key(aes_key, public_key):
    cipher = PKCS1_OAEP.new(public_key)
    return cipher.encrypt(aes_key)

def rsa_decrypt_key(encrypted_key, private_key):
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(encrypted_key)

# ── Week 6: SHA-256 (hash password + verify integrity) ────────────
def hash_password(password):
    salt = os.urandom(16).hex()
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return salt, hashed

def verify_password(password, salt, hashed):
    return hashlib.sha256((salt + password).encode()).hexdigest() == hashed

def sha256_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

# ── User Database ─────────────────────────────────────────────────
user_db = {}

def register():
    print("\n--- Student Registration ---")
    username = input("Enter username: ")
    password = input("Enter password: ")
    salt, hashed = hash_password(password)
    rsa_key = RSA.generate(2048)
    user_db[username] = {
        "salt"        : salt,
        "hash"        : hashed,
        "private_key" : rsa_key,
        "public_key"  : rsa_key.publickey()
    }
    print(f"[OK] User '{username}' registered.")
    print(f"[OK] Password Hash : {hashed[:40]}...")
    print(f"[OK] RSA key pair generated for {username}.")

def login():
    print("\n--- Student Login ---")
    username = input("Enter username: ")
    password = input("Enter password: ")
    if username not in user_db:
        print("[FAIL] User not found.")
        return None
    user = user_db[username]
    if verify_password(password, user["salt"], user["hash"]):
        print(f"[OK] Login successful. Welcome {username}!")
        return username
    else:
        print("[FAIL] Wrong password. Access denied.")
        return None

# ── Submit Report ─────────────────────────────────────────────────
submissions = {}

def submit_report(username):
    print("\n--- Submit Report ---")
    report_title = input("Enter report title: ")
    report_content = input("Enter report content: ")

    # Week 6: integrity hash
    integrity_hash = sha256_hash(report_content)
    print(f"\n[SHA-256] Integrity Hash : {integrity_hash[:40]}...")

    # Week 4: AES encrypt content
    aes_key = get_random_bytes(32)
    iv, encrypted_content = aes_encrypt(report_content, aes_key)
    print(f"[AES]     Report encrypted successfully.")

    # Week 5: RSA protect AES key
    public_key = user_db[username]["public_key"]
    encrypted_aes_key = rsa_encrypt_key(aes_key, public_key)
    print(f"[RSA]     AES key protected with RSA public key.")

    # Week 2: Caesar encode filename
    encoded_title = caesar_encrypt(report_title)
    print(f"[Caesar]  Encoded filename : {encoded_title}")

    # Week 3: RC4 encrypt metadata
    metadata = f"Submitted by: {username} | Title: {report_title} | Hash: {integrity_hash[:20]}"
    encrypted_metadata = rc4(username, metadata)
    print(f"[RC4]     Metadata encrypted.")

    # Store submission
    submissions[encoded_title] = {
        "iv"                 : iv,
        "encrypted_content"  : encrypted_content,
        "encrypted_aes_key"  : encrypted_aes_key,
        "encrypted_metadata" : encrypted_metadata,
        "integrity_hash"     : integrity_hash,
        "owner"              : username
    }

    print(f"\n[OK] Report '{report_title}' submitted and secured successfully.")

# ── Retrieve Report ───────────────────────────────────────────────
def retrieve_report(username):
    print("\n--- Retrieve Report ---")
    report_title = input("Enter report title to retrieve: ")
    encoded_title = caesar_encrypt(report_title)

    if encoded_title not in submissions:
        print("[FAIL] Report not found.")
        return

    submission = submissions[encoded_title]

    if submission["owner"] != username:
        print("[FAIL] Access denied. This report belongs to another user.")
        return

    # Week 5: RSA decrypt AES key
    private_key = user_db[username]["private_key"]
    aes_key = rsa_decrypt_key(submission["encrypted_aes_key"], private_key)
    print(f"[RSA]     AES key decrypted using private key.")

    # Week 4: AES decrypt content
    content = aes_decrypt(submission["iv"], submission["encrypted_content"], aes_key)
    print(f"[AES]     Report decrypted successfully.")

    # Week 6: verify integrity
    current_hash = sha256_hash(content)
    if current_hash == submission["integrity_hash"]:
        print(f"[SHA-256] Integrity check PASSED — report not tampered.")
    else:
        print(f"[SHA-256] Integrity check FAILED — report may be tampered!")

    # Week 3: RC4 decrypt metadata
    metadata = rc4(username, submission["encrypted_metadata"])
    print(f"[RC4]     Metadata : {metadata}")

    # Week 2: decode filename
    decoded_title = caesar_decrypt(encoded_title)
    print(f"[Caesar]  Decoded filename : {decoded_title}")

    print(f"\n--- Report Content ---\n{content}")

# ── Main Menu ─────────────────────────────────────────────────────
def main():
    print("=" * 50)
    print("  Secure Student Report Submission System")
    print("         BIT4138 Advanced Cryptography")
    print("=" * 50)

    while True:
        print("\n  1. Register")
        print("  2. Login and Submit Report")
        print("  3. Login and Retrieve Report")
        print("  0. Exit")
        choice = input("\nSelect option: ").strip()

        if choice == "1":
            register()
        elif choice == "2":
            user = login()
            if user:
                submit_report(user)
        elif choice == "3":
            user = login()
            if user:
                retrieve_report(user)
        elif choice == "0":
            print("\nGoodbye.")
            break
        else:
            print("[Error] Invalid option.")

main()
