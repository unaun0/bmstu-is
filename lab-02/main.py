from cryptography.hazmat.primitives import padding, ciphers
from cryptography.hazmat.backends import default_backend

BLOCK_SIZE = 128

def read_file(filename):
    with open(filename, "rb") as f:
        return f.read()

def write_file(filename, data):
    with open(filename, "wb") as f:
        f.write(data)

def encrypt_file(input_filename, encrypted_filename, key):
    data = read_file(input_filename)

    padder = padding.PKCS7(BLOCK_SIZE).padder()
    padded_data = padder.update(data) + padder.finalize()

    cipher = ciphers.Cipher(
        ciphers.algorithms.AES(key),
        ciphers.modes.ECB(),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()

    write_file(encrypted_filename, encrypted)

def decrypt_file(encrypted_filename, decrypted_filename, key):
    encrypted_data = read_file(encrypted_filename)

    cipher = ciphers.Cipher(
        ciphers.algorithms.AES(key),
        ciphers.modes.ECB(),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(BLOCK_SIZE).unpadder()
    decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()

    write_file(decrypted_filename, decrypted)

if __name__ == "__main__":
    input_filename = "sources/input.txt"
    encrypted_filename = "sources/encrypted.bin"
    decrypted_filename = "sources/decrypted.txt"
    key_filename = "sources/key.bin"

    # Читаем ключ из файла
    AES_KEY = read_file(key_filename)
    if len(AES_KEY) not in (16, 24, 32):
        raise ValueError("Ключ должен быть 16, 24 или 32 байта для AES")

    encrypt_file(input_filename, encrypted_filename, AES_KEY)
    decrypt_file(encrypted_filename, decrypted_filename, AES_KEY)
