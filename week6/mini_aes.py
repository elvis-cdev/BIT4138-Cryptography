# BIT4138 - Week 6: Challenge Task
# Mini AES-Inspired Encryption Simulator

# ── S-Box (4x4 AES-inspired) ──────────────────────────────────────
SBOX = {
    0:14, 1:4,  2:13, 3:1,
    4:2,  5:15, 6:11, 7:8,
    8:3,  9:10, 10:6, 11:12,
    12:5, 13:9, 14:0, 15:7
}
SBOX_INV = {v: k for k, v in SBOX.items()}

# ── Key Schedule ──────────────────────────────────────────────────
def generate_round_keys(key, rounds):
    round_keys = [key]
    for i in range(1, rounds + 1):
        round_keys.append((round_keys[-1] ^ (i * 13)) % 16)
    return round_keys

# ── Key Mixing ────────────────────────────────────────────────────
def key_mix(state, round_key):
    return state ^ round_key

# ── Substitution ──────────────────────────────────────────────────
def substitute(state):
    return SBOX[state % 16]

def substitute_inv(state):
    return SBOX_INV[state % 16]

# ── Permutation ───────────────────────────────────────────────────
def permute(state):
    bits = list(format(state, '04b'))
    permuted = [bits[1], bits[3], bits[0], bits[2]]
    return int(''.join(permuted), 2)

def permute_inv(state):
    bits = list(format(state, '04b'))
    restored = [bits[2], bits[0], bits[3], bits[1]]
    return int(''.join(restored), 2)

# ── Encryption ────────────────────────────────────────────────────
def encrypt(plaintext, key, rounds=4):
    state = plaintext % 16
    round_keys = generate_round_keys(key % 16, rounds)

    print(f"\n[AES-Mini] Plaintext  : {state:04b} ({state})")
    print(f"[AES-Mini] Key        : {key % 16:04b} ({key % 16})")
    print(f"[AES-Mini] Rounds     : {rounds}")

    for r in range(rounds):
        print(f"\n  --- Round {r+1} ---")
        state = key_mix(state, round_keys[r])
        print(f"  [Key Mix]     → {state:04b} ({state})")
        state = substitute(state)
        print(f"  [S-Box]       → {state:04b} ({state})")
        state = permute(state)
        print(f"  [Permute]     → {state:04b} ({state})")

    # Final key mixing
    state = key_mix(state, round_keys[rounds])
    print(f"\n  [Final Key Mix] → {state:04b} ({state})")
    return state

# ── Decryption ────────────────────────────────────────────────────
def decrypt(ciphertext, key, rounds=4):
    state = ciphertext
    round_keys = generate_round_keys(key % 16, rounds)

    print(f"\n[AES-Mini] Ciphertext : {state:04b} ({state})")
    state = key_mix(state, round_keys[rounds])

    for r in range(rounds - 1, -1, -1):
        print(f"\n  --- Decrypt Round {rounds - r} ---")
        state = permute_inv(state)
        print(f"  [Inv Permute] → {state:04b} ({state})")
        state = substitute_inv(state)
        print(f"  [Inv S-Box]   → {state:04b} ({state})")
        state = key_mix(state, round_keys[r])
        print(f"  [Key Mix]     → {state:04b} ({state})")

    return state

# ── Avalanche Effect ──────────────────────────────────────────────
def avalanche_test(p1, p2, key, rounds=4):
    c1 = encrypt(p1, key, rounds)
    c2 = encrypt(p2, key, rounds)
    in_diff  = bin(p1 ^ p2).count('1')
    out_diff = bin(c1 ^ c2).count('1')
    print(f"\n[Avalanche] Input  bits changed  : {in_diff}")
    print(f"[Avalanche] Output bits changed  : {out_diff}")
    print(f"[Avalanche] Effect : {'STRONG' if out_diff >= in_diff else 'WEAK'}")
    return c1, c2

# ── Main ──────────────────────────────────────────────────────────
print("=" * 50)
print("   Week 6 Challenge: Mini AES-Inspired Simulator")
print("=" * 50)

print("\n  1. Encrypt")
print("  2. Decrypt")
print("  3. Avalanche Test")
choice = input("\nSelect option: ").strip()

if choice == "1":
    p = int(input("Enter plaintext (0-15): "))
    k = int(input("Enter key (0-15): "))
    r = int(input("Enter rounds (2-4): "))
    c = encrypt(p, k, r)
    print(f"\n[Result] Ciphertext : {c:04b} ({c})")

elif choice == "2":
    c = int(input("Enter ciphertext (0-15): "))
    k = int(input("Enter key (0-15): "))
    r = int(input("Enter rounds (2-4): "))
    p = decrypt(c, k, r)
    print(f"\n[Result] Plaintext : {p:04b} ({p})")

elif choice == "3":
    p1 = int(input("Enter plaintext 1 (0-15): "))
    p2 = int(input("Enter plaintext 2 (0-15): "))
    k  = int(input("Enter key (0-15): "))
    r  = int(input("Enter rounds (2-4): "))
    avalanche_test(p1, p2, k, r)

print("\n" + "=" * 50)
