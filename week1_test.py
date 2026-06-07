from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)
msg = f.encrypt(b"BIT4138 Cryptography Setup Complete")
print("Encrypted:", msg)
print("Decrypted:", f.decrypt(msg).decode())
