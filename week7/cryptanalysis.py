# BIT4138 - Week 7: Block Cipher Cryptanalysis
# Algebraic Attacks, Differential and Linear Cryptanalysis

from collections import Counter
import random

# ── Simple XOR Cipher (target for analysis) ───────────────────────
def xor_encrypt(plaintext, key):
    return plaintext ^ key

# ── 1. Algebraic Attack Demo ──────────────────────────────────────
def algebraic_attack(plaintext, ciphertext):
    recovered_key = plaintext ^ ciphertext
    return recovered_key

# ── 2. Differential Cryptanalysis ────────────────────────────────
def differential_analysis(p1, p2, key):
    c1 = xor_encrypt(p1, key)
    c2 = xor_encrypt(p2, key)
    input_diff  = p1 ^ p2
    output_diff = c1 ^ c2
    return c1, c2, input_diff, output_diff

# ── 3. Avalanche Effect ───────────────────────────────────────────
def avalanche_effect(p1, p2, key):
    c1 = xor_encrypt(p1, key)
    c2 = xor_encrypt(p2, key)
    input_bits_changed  = bin(p1 ^ p2).count('1')
    output_bits_changed = bin(c1 ^ c2).count('1')
    return c1, c2, input_bits_changed, output_bits_changed

# ── 4. Frequency Analysis ─────────────────────────────────────────
def frequency_analysis(data):
    return Counter(data)

# ── 5. Linear Cryptanalysis (probability) ─────────────────────────
def linear_approximation(samples):
    successes = sum(1 for p, c, k in samples if (p ^ c) == k)
    probability = successes / len(samples)
    bias = abs(probability - 0.5)
    return probability, bias

# ── Main ──────────────────────────────────────────────────────────
print("=" * 50)
print("   Week 7: Block Cipher Cryptanalysis")
print("=" * 50)

# Algebraic Attack
print("\n--- 1. Algebraic Attack ---")
plaintext  = int(input("Enter plaintext  (0-255): "))
key        = int(input("Enter secret key (0-255): "))
ciphertext = xor_encrypt(plaintext, key)
print(f"[XOR] Plaintext  : {plaintext}")
print(f"[XOR] Key        : {key}")
print(f"[XOR] Ciphertext : {ciphertext}")
recovered  = algebraic_attack(plaintext, ciphertext)
print(f"[Algebraic] Recovered Key : {recovered}")
print(f"[Algebraic] Attack {'SUCCESSFUL' if recovered == key else 'FAILED'}")

# Differential Cryptanalysis
print("\n--- 2. Differential Cryptanalysis ---")
p1 = int(input("Enter plaintext 1 (0-255): "))
p2 = int(input("Enter plaintext 2 (0-255): "))
c1, c2, in_diff, out_diff = differential_analysis(p1, p2, key)
print(f"[Diff] Plaintext 1   : {p1:08b} ({p1})")
print(f"[Diff] Plaintext 2   : {p2:08b} ({p2})")
print(f"[Diff] Ciphertext 1  : {c1:08b} ({c1})")
print(f"[Diff] Ciphertext 2  : {c2:08b} ({c2})")
print(f"[Diff] Input  diff   : {in_diff:08b}")
print(f"[Diff] Output diff   : {out_diff:08b}")

# Avalanche Effect
print("\n--- 3. Avalanche Effect ---")
c1, c2, in_bits, out_bits = avalanche_effect(p1, p2, key)
print(f"[Avalanche] Input  bits changed : {in_bits}")
print(f"[Avalanche] Output bits changed : {out_bits}")
print(f"[Avalanche] Effect {'STRONG' if out_bits > in_bits else 'WEAK'}")

# Frequency Analysis
print("\n--- 4. Frequency Analysis ---")
data = "ABABABABCCCCDDDEEEFFF"
freq = frequency_analysis(data)
print(f"[Frequency] Data    : {data}")
print(f"[Frequency] Counts  : {dict(freq)}")
print(f"[Frequency] Bias detected in: {freq.most_common(1)[0][0]} (appears {freq.most_common(1)[0][1]} times)")

# Linear Cryptanalysis
print("\n--- 5. Linear Cryptanalysis ---")
secret_key = key
samples = [(random.randint(0,255), xor_encrypt(random.randint(0,255), secret_key), secret_key) for _ in range(100)]
prob, bias = linear_approximation(samples)
print(f"[Linear] Samples analysed : 100")
print(f"[Linear] Probability      : {prob:.2f}")
print(f"[Linear] Statistical bias : {bias:.2f}")
print(f"[Linear] Cipher appears   : {'WEAK (bias detected)' if bias > 0.1 else 'STRONG (no significant bias)'}")

print("\n" + "=" * 50)
