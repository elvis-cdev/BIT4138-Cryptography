# BIT4138 - Week 7: Challenge Task
# Block Cipher Security Analyzer

from collections import Counter
import random

# ── XOR Cipher (target cipher) ────────────────────────────────────
def xor_encrypt(plaintext, key):
    return plaintext ^ key

# ── 1. Avalanche Effect Test ──────────────────────────────────────
def avalanche_test(key, rounds=8):
    print("\n[Avalanche Effect Test]")
    print(f"  {'Plaintext 1':<15} {'Plaintext 2':<15} {'In Bits':<10} {'Out Bits':<10} {'Effect'}")
    print("  " + "-" * 60)
    for _ in range(rounds):
        p1 = random.randint(0, 255)
        p2 = p1 ^ (1 << random.randint(0, 7))
        c1 = xor_encrypt(p1, key)
        c2 = xor_encrypt(p2, key)
        in_diff  = bin(p1 ^ p2).count('1')
        out_diff = bin(c1 ^ c2).count('1')
        effect   = "STRONG" if out_diff >= in_diff else "WEAK"
        print(f"  {p1:<15} {p2:<15} {in_diff:<10} {out_diff:<10} {effect}")

# ── 2. Difference Analysis ────────────────────────────────────────
def difference_analysis(pairs, key):
    print("\n[Difference Analysis]")
    print(f"  {'P1':<8} {'P2':<8} {'C1':<8} {'C2':<8} {'In XOR':<10} {'Out XOR'}")
    print("  " + "-" * 55)
    for p1, p2 in pairs:
        c1 = xor_encrypt(p1, key)
        c2 = xor_encrypt(p2, key)
        in_xor  = p1 ^ p2
        out_xor = c1 ^ c2
        print(f"  {p1:<8} {p2:<8} {c1:<8} {c2:<8} {in_xor:<10} {out_xor}")

# ── 3. Frequency Distribution ─────────────────────────────────────
def frequency_distribution(key, samples=200):
    print("\n[Frequency Distribution]")
    ciphertexts = [xor_encrypt(random.randint(0, 255), key) for _ in range(samples)]
    freq = Counter(ciphertexts)
    top5 = freq.most_common(5)
    print(f"  Samples analysed : {samples}")
    print(f"  Top 5 most frequent ciphertext values:")
    for val, count in top5:
        bar = "#" * count
        print(f"  {val:>4} : {count:>4} times  |{bar[:40]}")
    expected = samples / 256
    bias = max(count for _, count in top5) - expected
    print(f"\n  Expected frequency : {expected:.2f}")
    print(f"  Max bias detected  : {bias:.2f}")
    print(f"  Cipher appears     : {'WEAK (bias detected)' if bias > 5 else 'STRONG (uniform distribution)'}")

# ── 4. Statistical Bias Report ────────────────────────────────────
def statistical_bias(key, samples=500):
    print("\n[Statistical Bias Report]")
    results = []
    for _ in range(samples):
        p = random.randint(0, 255)
        c = xor_encrypt(p, key)
        results.append((p ^ c) == key)
    successes  = sum(results)
    probability = successes / samples
    bias        = abs(probability - 0.5)
    print(f"  Samples    : {samples}")
    print(f"  Successes  : {successes}")
    print(f"  Probability: {probability:.4f}  (ideal = 0.5000)")
    print(f"  Bias       : {bias:.4f}  (ideal = 0.0000)")
    print(f"  Verdict    : {'WEAK — key relationship exposed' if bias > 0.1 else 'STRONG — no significant bias'}")

# ── 5. Full Security Report ───────────────────────────────────────
def security_report(key):
    print("\n" + "=" * 50)
    print("         FULL SECURITY ANALYSIS REPORT")
    print("=" * 50)
    print(f"  Cipher       : XOR Block Cipher")
    print(f"  Key          : {key}")
    print(f"  Key (binary) : {key:08b}")

    # Quick checks
    c1 = xor_encrypt(100, key)
    c2 = xor_encrypt(101, key)
    avalanche = bin(c1 ^ c2).count('1')

    ciphers    = [xor_encrypt(i, key) for i in range(256)]
    unique     = len(set(ciphers))
    freq       = Counter(ciphers)
    max_freq   = freq.most_common(1)[0][1]

    print(f"\n  [1] Avalanche Effect    : {avalanche} bit(s) changed  → {'PASS' if avalanche >= 1 else 'FAIL'}")
    print(f"  [2] Output Uniqueness   : {unique}/256 unique values → {'PASS' if unique == 256 else 'FAIL'}")
    print(f"  [3] Max Frequency Bias  : {max_freq} occurrences     → {'PASS' if max_freq == 1 else 'FAIL'}")
    print(f"\n  Overall Security Rating : {'STRONG' if avalanche >= 1 and unique == 256 else 'WEAK'}")
    print("=" * 50)

# ── Main ──────────────────────────────────────────────────────────
print("=" * 50)
print("  Week 7 Challenge: Block Cipher Security Analyzer")
print("=" * 50)

key = int(input("\nEnter secret key (0-255): "))

print("\n  1. Avalanche Effect Test")
print("  2. Difference Analysis")
print("  3. Frequency Distribution")
print("  4. Statistical Bias Report")
print("  5. Full Security Report")
print("  6. Run All")
choice = input("\nSelect option: ").strip()

if choice == "1":
    avalanche_test(key)

elif choice == "2":
    pairs = [(10,11),(50,51),(100,101),(200,201),(75,76)]
    difference_analysis(pairs, key)

elif choice == "3":
    frequency_distribution(key)

elif choice == "4":
    statistical_bias(key)

elif choice == "5":
    security_report(key)

elif choice == "6":
    avalanche_test(key)
    pairs = [(10,11),(50,51),(100,101),(200,201),(75,76)]
    difference_analysis(pairs, key)
    frequency_distribution(key)
    statistical_bias(key)
    security_report(key)

print("\n" + "=" * 50)
