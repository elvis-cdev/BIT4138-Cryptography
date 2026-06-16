# BIT4138 - Week 6: Symmetric Ciphers II
# Substitution-Permutation Networks, S-Boxes and Non-Linearity

# ── S-Box (Substitution Box) ──────────────────────────────────────
SBOX = {
    0: 14, 1: 4,  2: 13, 3: 1,
    4: 2,  5: 15, 6: 11, 7: 8,
    8: 3,  9: 10, 10: 6, 11: 12,
    12: 5, 13: 9, 14: 0, 15: 7
}

SBOX_INV = {v: k for k, v in SBOX.items()}

# ── Permutation Table ─────────────────────────────────────────────
PBOX = [1, 5, 2, 0, 3, 7, 4, 6]

# ── Substitution ──────────────────────────────────────────────────
def substitute(nibble):
    return SBOX[nibble]

def substitute_inv(nibble):
    return SBOX_INV[nibble]

# ── Permutation ───────────────────────────────────────────────────
def permute(bits):
    return [bits[PBOX[i]] for i in range(len(bits))]

def int_to_bits(n, length=4):
    return [int(b) for b in format(n, f'0{length}b')]

def bits_to_int(bits):
    return int(''.join(str(b) for b in bits), 2)

# ── Key Mixing ────────────────────────────────────────────────────
def key_mix(plaintext, key):
    return plaintext ^ key

# ── Single SPN Round ──────────────────────────────────────────────
def spn_round(plaintext, round_key):
    # Step 1: Key mixing
    mixed = key_mix(plaintext, round_key)
    print(f"  [Key Mix]     {plaintext:04b} XOR {round_key:04b} = {mixed:04b} ({mixed})")

    # Step 2: Substitution
    substituted = substitute(mixed)
    print(f"  [S-Box]       {mixed} → {substituted}")

    # Step 3: Permutation
    bits = int_to_bits(substituted)
    permuted_bits = permute(bits)
    permuted = bits_to_int(permuted_bits)
    print(f"  [Permutation] {''.join(map(str,bits))} → {''.join(map(str,permuted_bits))} ({permuted})")

    return permuted

# ── Multi-Round SPN ───────────────────────────────────────────────
def spn_encrypt(plaintext, key, rounds=3):
    state = plaintext
    round_keys = [(key + i) % 16 for i in range(rounds)]
    print(f"\n[SPN] Encrypting {plaintext} over {rounds} rounds")
    for r in range(rounds):
        print(f"\n  --- Round {r+1} ---")
        state = spn_round(state, round_keys[r])
    return state

# ── Avalanche Effect ──────────────────────────────────────────────
def avalanche_test(p1, p2, key):
    c1 = spn_encrypt(p1, key)
    c2 = spn_encrypt(p2, key)
    diff_input  = bin(p1 ^ p2).count('1')
    diff_output = bin(c1 ^ c2).count('1')
    print(f"\n[Avalanche Test]")
    print(f"  Plaintext 1   : {p1:04b} ({p1})")
    print(f"  Plaintext 2   : {p2:04b} ({p2})")
    print(f"  Input  diff   : {diff_input} bit(s) changed")
    print(f"  Ciphertext 1  : {c1:04b} ({c1})")
    print(f"  Ciphertext 2  : {c2:04b} ({c2})")
    print(f"  Output diff   : {diff_output} bit(s) changed")
    return c1, c2

# ── Non-Linearity Demo ────────────────────────────────────────────
def nonlinearity_demo():
    print("\n[Non-Linearity Demo]")
    print("  Input | S-Box Output | Binary")
    print("  " + "-" * 30)
    for i in range(8):
        out = SBOX[i]
        print(f"  {i:5} | {out:12} | {out:04b}")
    print("  (Outputs are not linear — no simple formula predicts them)")

# ── Main ──────────────────────────────────────────────────────────
print("=" * 50)
print("   Week 6: SPN, S-Boxes and Non-Linearity")
print("=" * 50)

# S-Box demo
print("\n--- S-Box Substitution ---")
val = int(input("Enter a value (0-15) to substitute: "))
print(f"[S-Box] Input: {val} → Output: {SBOX[val]}")

# Full SPN encryption
print("\n--- SPN Encryption ---")
plaintext = int(input("Enter plaintext (0-15): "))
key = int(input("Enter key (0-15): "))
ciphertext = spn_encrypt(plaintext, key)
print(f"\n[SPN] Final Ciphertext: {ciphertext}")

# Avalanche effect
print("\n--- Avalanche Effect Test ---")
p1 = int(input("Enter first plaintext (0-15): "))
p2 = int(input("Enter second plaintext (0-15, differ by 1 bit): "))
avalanche_test(p1, p2, key)

# Non-linearity
nonlinearity_demo()

print("\n" + "=" * 50)
