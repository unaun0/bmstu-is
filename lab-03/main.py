from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os

KEY_FILE = "sources/des_key.key"

def generate_key():
    key = get_random_bytes(8)
    os.makedirs(os.path.dirname(KEY_FILE), exist_ok=True)
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key

def load_key():
    with open(KEY_FILE, "rb") as f:
        return f.read()

def encrypt_file_ecb(input_path, output_path, key):
    cipher = DES.new(key, DES.MODE_ECB)  # ECB
    with open(input_path, "rb") as f:
        data = f.read()
    ciphertext = cipher.encrypt(pad(data, DES.block_size))
    with open(output_path, "wb") as f:
        f.write(ciphertext)
    print(f"Файл {input_path} зашифрован в {output_path}")

def decrypt_file_ecb(input_path, output_path, key):
    cipher = DES.new(key, DES.MODE_ECB)
    with open(input_path, "rb") as f:
        ciphertext = f.read()
    data = unpad(cipher.decrypt(ciphertext), DES.block_size)
    with open(output_path, "wb") as f:
        f.write(data)
    print(f"Файл {input_path} расшифрован в {output_path}")

if __name__ == "__main__":
    input_file = "sources/input.txt"
    enc_file = "sources/encrypted.bin"
    dec_file = "sources/decrypted.txt"

    key = generate_key() if not os.path.exists(KEY_FILE) else load_key()

    encrypt_file_ecb(input_file, enc_file, key)
    decrypt_file_ecb(enc_file, dec_file, key)
