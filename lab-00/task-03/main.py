import math
from collections import Counter

# --- Функции преобразования ---

def text_to_bits(text):
    return [int(b) for c in text for b in format(ord(c), "08b")]

def bits_to_text(bits):
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return "".join(chr(int("".join(map(str, b)), 2)) for b in chars)

def format_bits(bit_array, order):
  bit_string = ''.join(map(str, bit_array))  # Convert to a string first
  return ' '.join([bit_string[i:i+8] for i in range(0, len(bit_string), order)])

# --- Шифрование Фейстеля ---

def shift_cipher(bits, k):
    k = k % len(bits)
    return bits[k:] + bits[:k]

def xor_bits(a, b):
    return [x ^ y for x, y in zip(a, b)]

def feistel_round(L, R, k):
    f_out = shift_cipher(L, k)
    new_R = xor_bits(R, f_out)
    return new_R, L

def feistel_encrypt(block, keys):
    bits = text_to_bits(block)
    print(format_bits(bits, 8))
    mid = len(bits) // 2
    L, R = bits[:mid], bits[mid:]
    for k in keys:
        L, R = feistel_round(L, R, k)
    return bits_to_text(L + R)

def feistel_decrypt(block, keys):
    bits = text_to_bits(block)
    mid = len(bits) // 2
    L, R = bits[:mid], bits[mid:]
    for k in reversed(keys):
        R, L = feistel_round(R, L, k)
    return bits_to_text(L + R)

# --- Тесты случайности ---

def frequency_test(bits):
    count0 = bits.count(0)
    count1 = bits.count(1)
    total = len(bits)
    return {
        "zeros": count0,
        "ones": count1,
        "ratio": count1 / total
    }

def chi_square_test(bits):
    counts = Counter(bits)
    expected = len(bits) / 2
    chi2 = sum((counts[b] - expected) ** 2 / expected for b in [0, 1])
    return chi2

def poker_test(bits, m=4):
    if len(bits) % m != 0:
        bits = bits[:len(bits) - (len(bits) % m)]
    patterns = [bits[i:i+m] for i in range(0, len(bits), m)]
    pattern_counts = Counter(tuple(p) for p in patterns)
    N = len(patterns)
    X2 = (len(pattern_counts) / N) * sum(count**2 for count in pattern_counts.values()) - N
    return X2

def correlation_test(bits1, bits2):
    if len(bits1) != len(bits2):
        min_len = min(len(bits1), len(bits2))
        bits1, bits2 = bits1[:min_len], bits2[:min_len]
    mean1 = sum(bits1) / len(bits1)
    mean2 = sum(bits2) / len(bits2)
    numerator = sum((b1 - mean1) * (b2 - mean2) for b1, b2 in zip(bits1, bits2))
    denominator = math.sqrt(sum((b1 - mean1)**2 for b1 in bits1) * sum((b2 - mean2)**2 for b2 in bits2))
    return numerator / denominator if denominator != 0 else 0

# --- Демонстрация ---

plaintext = "AVADAKEDAVRA"
keys = [1, 2, 3, 4]

blocks = [plaintext[i:i+6] for i in range(0, len(plaintext), 6)]
cipher_blocks = [feistel_encrypt(b, keys) for b in blocks]
ciphertext = "".join(cipher_blocks)

cipher_bits = text_to_bits(ciphertext)
plain_bits = text_to_bits(plaintext)

freq = frequency_test(cipher_bits)
chi2 = chi_square_test(cipher_bits)
poker = poker_test(cipher_bits)
corr = correlation_test(plain_bits, cipher_bits)

print("Plaintext :", plaintext)
print("Ciphertext:", ciphertext)
print("Plaintext (bin):", format_bits(text_to_bits(plaintext), 8))
print("Ciphertext(bin):", format_bits(text_to_bits(ciphertext), 8))
print("Decrypted :", "".join(feistel_decrypt(b, keys) for b in cipher_blocks))

print("\n--- Тесты псевдослучайности ---")
print("Frequency test:", freq)
print("Chi-square    :", chi2)
print("Poker test    :", poker)
print("Correlation   :", corr)