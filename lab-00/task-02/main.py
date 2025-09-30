from collections import Counter

INPUT_FILENAME = 'encrypted.txt'

RUSSIAN_FREQUENCIES = {
    'о': 0.1097, 'е': 0.0845, 'а': 0.0801, 'и': 0.0735, 'н': 0.0670,
    'т': 0.0626, 'с': 0.0547, 'р': 0.0473, 'в': 0.0454, 'л': 0.0440,
    'к': 0.0349, 'м': 0.0321, 'д': 0.0298, 'п': 0.0281, 'у': 0.0262,
    'я': 0.0201, 'ы': 0.0190, 'ь': 0.0174, 'г': 0.0170, 'з': 0.0165,
    'б': 0.0159, 'ч': 0.0144, 'й': 0.0121, 'х': 0.0097, 'ж': 0.0094,
    'ш': 0.0073, 'ю': 0.0064, 'ц': 0.0048, 'щ': 0.0036, 'э': 0.0032,
    'ф': 0.0026, 'ъ': 0.0004, 'ё': 0.0004
}

RUSSIAN_LETTERS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

def read_from_file(filename):
    with open(file=filename, mode='r') as f:
        data = f.read()
    return data

def frequency_analysis(text):
    text = text.lower()
    text_letters = [c for c in text if c in RUSSIAN_LETTERS]
    total_letters = len(text_letters)

    freqs = Counter(text_letters)
    text_freqs = {char: count / total_letters for char, count in freqs.items()}

    sorted_text = sorted(text_freqs, key=text_freqs.get, reverse=True)
    sorted_lang = sorted(RUSSIAN_FREQUENCIES, key=RUSSIAN_FREQUENCIES.get, reverse=True)

    mapping = {sorted_text[i]: sorted_lang[i] for i in range(min(len(sorted_text), len(sorted_lang)))}

    print("=== Сопоставление букв ===")
    for k, v in mapping.items():
        print(f"{k} → {v}")

    decrypted = ""
    for ch in text:
        if ch in mapping:
            decrypted += mapping[ch]
        else:
            decrypted += ch

    print("\n=== Дешифрованный текст (по частотам) ===\n")
    print(decrypted)

cipher_text = read_from_file(INPUT_FILENAME)
frequency_analysis(cipher_text)