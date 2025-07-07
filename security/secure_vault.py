import base64
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes

def encrypt(plaintext, password):
    salt = get_random_bytes(16)
    key = PBKDF2(password, salt, dkLen=32)
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode())

    encrypted_data = base64.b64encode(salt + cipher.nonce + tag + ciphertext).decode()
    return encrypted_data

def decrypt(encrypted_data, password):
    try:
        raw = base64.b64decode(encrypted_data)
        salt = raw[:16]
        nonce = raw[16:32]
        tag = raw[32:48]
        ciphertext = raw[48:]

        key = PBKDF2(password, salt, dkLen=32)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext.decode()
    except Exception:
        return None

def main():
    print("🔐 Secure Vault CLI (Visible Input)")
    print("===================================")

    while True:
        action = input("\nChoose [E]ncrypt, [D]ecrypt or [Q]uit: ").strip().lower()

        if action == 'q':
            print("Goodbye!")
            break

        elif action == 'e':
            secret = input("Enter the secret to encrypt (will be visible): ")
            master = input("Enter your master password (visible): ")
            encrypted = encrypt(secret, master)
            print("\n🔐 Encrypted secret (save this safely):")
            print(encrypted)

        elif action == 'd':
            encrypted_data = input("Paste the encrypted secret: ")
            master = input("Enter your master password (visible): ")
            decrypted = decrypt(encrypted_data, master)
            if decrypted is None:
                print("❌ Failed to decrypt. Wrong password or invalid data.")
            else:
                print("\n🔓 Decrypted secret:")
                print(decrypted)

        else:
            print("Invalid option. Please choose E, D, or Q.")

if __name__ == "__main__":
    main()
