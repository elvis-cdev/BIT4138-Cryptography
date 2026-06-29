"""
BIT4138 - Advanced Cryptography
Week 8 Practical Task 2: Diffie-Hellman Key Exchange Implementation
Student: Elvis
"""

def get_positive_int(prompt):
    """Helper to get a valid positive integer from user input."""
    while True:
        try:
            val = int(input(prompt))
            if val > 0:
                return val
            else:
                print("  Please enter a positive integer.")
        except ValueError:
            print("  Invalid input. Please enter an integer.")

def is_prime(n):
    """Basic primality check."""
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def diffie_hellman():
    print("=" * 55)
    print("   Diffie-Hellman Key Exchange - BIT4138 Week 8")
    print("=" * 55)

    # Step 1: Public Parameters
    print("\n[Step 1] Enter Public Parameters")
    while True:
        p = get_positive_int("  Enter a prime number (p): ")
        if is_prime(p):
            break
        print(f"  {p} is not prime. Please enter a prime number.")

    g = get_positive_int("  Enter a generator (g): ")
    print(f"\n  Public Prime  (p) = {p}")
    print(f"  Generator     (g) = {g}")

    # Step 2: Private Keys (kept secret)
    print("\n[Step 2] Enter Private Keys (kept secret)")
    alice_private = get_positive_int("  Alice's private key (a): ")
    bob_private   = get_positive_int("  Bob's private key   (b): ")

    # Step 3: Compute Public Keys
    alice_public = pow(g, alice_private, p)   # A = g^a mod p
    bob_public   = pow(g, bob_private,   p)   # B = g^b mod p

    print("\n[Step 3] Generated Public Keys")
    print(f"  Alice's public key (A = g^a mod p) = {alice_public}")
    print(f"  Bob's   public key (B = g^b mod p) = {bob_public}")

    # Step 4: Exchange and Compute Shared Secret
    alice_secret = pow(bob_public,   alice_private, p)  # S = B^a mod p
    bob_secret   = pow(alice_public, bob_private,   p)  # S = A^b mod p

    print("\n[Step 4] Computing Shared Secret")
    print(f"  Alice computes: S = B^a mod p = {bob_public}^{alice_private} mod {p} = {alice_secret}")
    print(f"  Bob   computes: S = A^b mod p = {alice_public}^{bob_private} mod {p} = {bob_secret}")

    # Step 5: Verify
    print("\n[Step 5] Verification")
    print("=" * 55)
    print(f"  Public Prime (p)  : {p}")
    print(f"  Generator    (g)  : {g}")
    print(f"  Alice Secret Key  : {alice_private}")
    print(f"  Bob   Secret Key  : {bob_private}")
    print(f"  Alice Public Key  : {alice_public}")
    print(f"  Bob   Public Key  : {bob_public}")
    print(f"  Alice Shared Secret: {alice_secret}")
    print(f"  Bob   Shared Secret: {bob_secret}")
    print("=" * 55)

    if alice_secret == bob_secret:
        print(f"\n  ✓ SUCCESS: Both parties share the same secret key: {alice_secret}")
    else:
        print("\n  ✗ ERROR: Shared secrets do not match. Check your inputs.")

    print("\n  Security Note:")
    print("  An attacker seeing g, p, A, B cannot recover the secret")
    print("  without solving the Discrete Logarithm Problem.")
    print("=" * 55)

if __name__ == "__main__":
    diffie_hellman()
