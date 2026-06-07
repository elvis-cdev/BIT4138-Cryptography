# BIT4138 - Week 3: Stream Ciphers and Randomness Testing

import random
import time

# ── 1. LFSR Generator ─────────────────────────────────────────────
def lfsr(seed, taps, length):
    state = seed
    sequence = []
    for _ in range(length):
        bit = 0
        for t in taps:
            bit ^= (state >> t) & 1
        state = ((state >> 1) | (bit << (len(bin(seed)) - 3))) & ((1 << (len(bin(seed)) - 2)) - 1)
        sequence.append(bit)
    return sequence

# ── 2. RC4 Stream Cipher ──────────────────────────────────────────
def rc4(key, plaintext):
    key = [ord(c) for c in key]
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    result = []
    for char in plaintext:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        result.append(chr(ord(char) ^ S[(S[i] + S[j]) % 256]))
    return ''.join(result)

# ── 3. Randomness Tests ───────────────────────────────────────────
def frequency_test(bits):
    ones = bits.count(1)
    zeros = bits.count(0)
    return ones, zeros

def runs_test(bits):
    runs = 1
    for i in range(1, len(bits)):
        if bits[i] != bits[i-1]:
            runs += 1
    return runs

def mean_test(bits):
    return sum(bits) / len(bits)

# ── Main ──────────────────────────────────────────────────────────
print("=" * 50)
print("   Week 3: Stream Ciphers & Randomness Testing")
print("=" * 50)

# LFSR sequence
seed = 0b10110
taps = [4, 2]
sequence = lfsr(seed, taps, 100)
print(f"\n[LFSR] Seed        : {bin(seed)}")
print(f"[LFSR] First 20    : {sequence[:20]}")
print(f"[LFSR] Full 100    : {sequence}")

# Randomness Tests
ones, zeros = frequency_test(sequence)
runs = runs_test(sequence)
mean = mean_test(sequence)
print(f"\n[Frequency Test]  Ones: {ones}   Zeros: {zeros}")
print(f"[Runs Test]       Total runs: {runs}")
print(f"[Mean Test]       Mean: {mean:.4f}  (ideal = 0.5000)")

# RC4 Encryption
print("\n--- RC4 Stream Cipher ---")
key = input("Enter RC4 key: ")
message = input("Enter message to encrypt: ")
encrypted = rc4(key, message)
decrypted = rc4(key, encrypted)
print(f"[RC4] Original  : {message}")
print(f"[RC4] Encrypted : {encrypted.encode()}")
print(f"[RC4] Decrypted : {decrypted}")

# Performance Test
print("\n--- Performance Test ---")
test_message = "A" * 10000
test_key = "TESTKEY"

start = time.time()
for _ in range(100):
    rc4(test_key, test_message)
end = time.time()

print(f"[RC4] Encrypted 10,000 chars x 100 iterations")
print(f"[RC4] Time taken : {end - start:.4f} seconds")
print(f"[RC4] Speed      : {(100 * len(test_message)) / (end - start):.0f} chars/second")

print("\n" + "=" * 50)
