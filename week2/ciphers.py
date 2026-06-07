# BIT4138 - Week 2: Classical Ciphers
# Caesar Cipher and Vigenere Cipher Implementation

def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

def vigenere_encrypt(text, key):
    result = ""
    key = key.upper()
    j = 0
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = ord(key[j % len(key)]) - ord('A')
            result += chr((ord(char) - base + shift) % 26 + base)
            j += 1
        else:
            result += char
    return result

def vigenere_decrypt(text, key):
    result = ""
    key = key.upper()
    j = 0
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift = ord(key[j % len(key)]) - ord('A')
            result += chr((ord(char) - base - shift) % 26 + base)
            j += 1
        else:
            result += char
    return result

def get_message():
    while True:
        msg = input("Enter message: ").strip()
        if msg == "":
            print("[Error] Message cannot be empty. Try again.")
        elif not any(c.isalpha() for c in msg):
            print("[Error] Message must contain at least one letter. Try again.")
        else:
            return msg

def get_shift():
    while True:
        try:
            shift = int(input("Enter Caesar shift (1-25): "))
            if 1 <= shift <= 25:
                return shift
            print("[Error] Shift must be between 1 and 25. Try again.")
        except ValueError:
            print("[Error] Invalid input. Enter a number. Try again.")

def get_key():
    while True:
        key = input("Enter Vigenere key (letters only): ").strip()
        if key == "":
            print("[Error] Key cannot be empty. Try again.")
        elif not key.isalpha():
            print("[Error] Key must contain letters only. Try again.")
        else:
            return key

# ---- Main ----
print("=" * 40)
print("   Week 2: Classical Cipher Program")
print("=" * 40)

message = get_message()

# Caesar
shift = get_shift()
c_enc = caesar_encrypt(message, shift)
c_dec = caesar_decrypt(c_enc, shift)
print(f"\n[Caesar] Encrypted : {c_enc}")
print(f"[Caesar] Decrypted : {c_dec}")

# Vigenere
key = get_key()
v_enc = vigenere_encrypt(message, key)
v_dec = vigenere_decrypt(v_enc, key)
print(f"\n[Vigenere] Encrypted : {v_enc}")
print(f"[Vigenere] Decrypted : {v_dec}")

print("\n" + "=" * 40)
