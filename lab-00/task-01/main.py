import os
import ast
import random

INPUT_FILENAME = 'input.txt'
ENCRYPTED_FILENAME = 'encrypted.txt'
DECRYPTED_FILENAME = 'decrypted.txt'
KEY_FILENAME = 'key.txt'

ALPHABET = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

def read_from_file(filename):
    with open(file=filename, mode='r') as f:
        data = f.read()
    return data

def write_to_file(filename, text):
    with open(file=filename, mode='w') as f:
        f.write(text)

def generate_key(alphabet):
    temp = list(alphabet)
    random.shuffle(temp)
    return dict(zip(alphabet, temp))

def key_from_file(filename):
    return ast.literal_eval(
        read_from_file(KEY_FILENAME)
    )

def encrypt(input_filename, output_filename, key_filename):
    input_text = read_from_file(input_filename)
    key = key_from_file(key_filename)
    encrypted_text = ""
    for c in input_text:
        try:
            encrypted_text += key[c]
        except:
            encrypted_text += c
    write_to_file(output_filename, encrypted_text)


def decrypt(input_filename, output_filename, key_filename):
    input_text = read_from_file(input_filename)
    key = key_from_file(key_filename)
    decrypted_text = ""
    for c in input_text:
        try:
            decrypted_text += next((k for k, v in key.items() if v == c.upper()), c)
        except:
            decrypted_text += c
    write_to_file(output_filename, decrypted_text)


def main():
    key = generate_key(ALPHABET)
    write_to_file(KEY_FILENAME, str(key))

    encrypt(INPUT_FILENAME, ENCRYPTED_FILENAME, KEY_FILENAME)

    decrypt(ENCRYPTED_FILENAME, DECRYPTED_FILENAME, KEY_FILENAME)

if __name__ == "__main__":
    main()