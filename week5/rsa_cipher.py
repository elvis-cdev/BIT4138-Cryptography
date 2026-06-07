# BIT4138 - Week 5: Public Key Cryptography (RSA)

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import time

def generate_keys():
    key = RSA.generate(2048)
    private_key = key
    public_key = key.publickey()
    return private_key, public_key

def encrypt_message(message, public_key):
    cipher = PKCS1_OAEP.new(public_key)
    return cipher.encrypt(message.encode())

def decrypt_message(ciphertext, private_key):
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(ciphertext).decode()

def save_keys(private_key, public_key):
    with open("week5/private.pem", "wb") as f:
        f.write(private_key.export_key())
    with open("week5/public.pem", "wb") as f:
        f.write(public_key.export_key())

# ── Main ──────────────────────────────────────────────────────────
print("=" * 50)
print("      Week 5: RSA Public Key Cryptography")
print("=" * 50)

# Key Generation
print("\n[RSA] Generating 2048-bit key pair...")
start = time.time()
private_key, public_key = generate_keys()
end = time.time()
print(f"[RSA] Key pair generated in {end - start:.4f} seconds")
print(f"[RSA] Public Key  :\n{public_key.export_key().decode()}")
print(f"[RSA] Private Key :\n{private_key.export_key().decode()[:200]}...")

# Save keys to files
save_keys(private_key, public_key)
print("\n[RSA] Keys saved to week5/private.pem and week5/public.pem")

# Encrypt and Decrypt
message = input("\nEnter message to encrypt: ")
ciphertext = encrypt_message(message, public_key)
print(f"\n[RSA] Encrypted : {ciphertext.hex()[:80]}...")
decrypted = decrypt_message(ciphertext, private_key)
print(f"[RSA] Decrypted : {decrypted}")

# Validation
print("\n--- Validation Test ---")
if message == decrypted:
    print("[PASS] Original and decrypted messages match exactly.")
else:
    print("[FAIL] Messages do not match.")

print("\n" + "=" * 50)

# ── Secure Message Simulation ─────────────────────────────────────
print("\n--- Secure Message Transmission: Alice to Bob ---")

# Bob generates his keys
print("[Bob]   Generating key pair...")
bob_private, bob_public = generate_keys()
print("[Bob]   Key pair ready. Sharing public key with Alice...")

# Alice encrypts using Bob's public key
alice_message = input("\n[Alice] Enter message to send to Bob: ")
alice_encrypted = encrypt_message(alice_message, bob_public)
print(f"[Alice] Message encrypted using Bob's public key.")
print(f"[Alice] Sending ciphertext : {alice_encrypted.hex()[:60]}...")

# Bob decrypts using his private key
bob_decrypted = decrypt_message(alice_encrypted, bob_private)
print(f"\n[Bob]   Decrypted message from Alice : {bob_decrypted}")
print("[Bob]   Secure transmission successful.")

print("\n" + "=" * 50)
