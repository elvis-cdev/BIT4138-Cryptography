# BIT4138 - Week 4: Block Cipher Design and AES

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import time
import os

def generate_key():
    return get_random_bytes(32)  # 256-bit key

def aes_encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return cipher.iv, ciphertext

def aes_decrypt(iv, ciphertext, key):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()

def encrypt_file(filename, key):
    with open(filename, 'r') as f:
        data = f.read()
    iv, ciphertext = aes_encrypt(data, key)
    with open(filename + '.enc', 'wb') as f:
        f.write(iv + ciphertext)
    return filename + '.enc'

def decrypt_file(filename, key):
    with open(filename, 'rb') as f:
        data = f.read()
    iv = data[:16]
    ciphertext = data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()

# ── Main ──────────────────────────────────────────────────────────
print("=" * 50)
print("      Week 4: AES Block Cipher")
print("=" * 50)

# Key generation
key = generate_key()
print(f"\n[AES] Key Generated  : {key.hex()}")
print(f"[AES] Key Size       : {len(key) * 8} bits")

# Encrypt and decrypt a message
message = input("\nEnter message to encrypt: ")
iv, ciphertext = aes_encrypt(message, key)
decrypted = aes_decrypt(iv, ciphertext, key)
print(f"\n[AES] Original       : {message}")
print(f"[AES] Encrypted      : {ciphertext.hex()}")
print(f"[AES] Decrypted      : {decrypted}")

# File encryption
print("\n--- File Encryption ---")
with open("week4/testfile.txt", "w") as f:
    f.write("BIT4138 AES File Encryption Test\nMount Kenya University\nAdvanced Cryptography")

enc_file = encrypt_file("week4/testfile.txt", key)
print(f"[AES] File encrypted : {enc_file}")
recovered = decrypt_file(enc_file, key)
print(f"[AES] File decrypted :\n{recovered}")

# Performance Test
print("\n--- Performance Test ---")
test_data = "A" * 10000
start = time.time()
for _ in range(100):
    iv, ct = aes_encrypt(test_data, key)
end = time.time()
print(f"[AES] Encrypted 10,000 chars x 100 iterations")
print(f"[AES] Time taken     : {end - start:.4f} seconds")
print(f"[AES] Speed          : {(100 * len(test_data)) / (end - start):.0f} chars/second")

print("\n" + "=" * 50)
