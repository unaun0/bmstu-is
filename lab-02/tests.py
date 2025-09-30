import numpy as np
from statsmodels.stats.diagnostic import acorr_ljungbox
from scipy.stats import chisquare

# === Функция для чтения бинарного файла в массив битов ===
def read_bin_file_bits(filename):
    with open(filename, "rb") as f:
        data = f.read()
    bits = []
    for byte in data:
        for i in range(8):
            bits.append((byte >> (7 - i)) & 1)
    return bits

# === Автокорреляционный тест ===
def autocorrelation_test(bits):
    print("\n=== Автокорреляционный тест ===")
    bits_array = np.array(bits)
    result = acorr_ljungbox(bits_array, lags=[10], return_df=True)
    p_value = result['lb_pvalue'].values[0]
    print(result)

    if p_value > 0.5:
        comment = "Хорошо — случайность сильная"
    elif p_value > 0.05:
        comment = "Нормально — случайность допустима"
    else:
        comment = "Плохо — возможна корреляция"
    print(f"Комментарий: {comment}")

# === Покерный тест ===
def poker_test(bits, m=4):
    print("\n=== Покерный тест ===")
    n = len(bits) // m
    counts = {}
    for i in range(n):
        chunk = bits[i*m:(i+1)*m]
        key = "".join(str(b) for b in chunk)
        counts[key] = counts.get(key, 0) + 1

    all_patterns = [format(i, f"0{m}b") for i in range(2**m)]
    observed = [counts.get(p, 0) for p in all_patterns]
    expected_count = n / (2**m)
    expected = [expected_count] * len(all_patterns)

    chi2_stat, p_val = chisquare(observed, expected)
    print(f"Chi2 Stat: {chi2_stat}, P-Value: {p_val}")

    if p_val > 0.5:
        comment = "Хорошо — распределение близко к равномерному"
    elif p_val > 0.05:
        comment = "Нормально — небольшие отклонения допустимы"
    else:
        comment = "Плохо — распределение неравномерное"
    print(f"Комментарий: {comment}")

# === Хи²-тест ===
def chi_square_test(bits):
    print("\n=== Хи²-тест ===")
    counts = [bits.count(0), bits.count(1)]
    expected = [len(bits) / 2, len(bits) / 2]
    chi2_stat, p_val = chisquare(counts, expected)
    print(f"Chi2 Stat: {chi2_stat}, P-Value: {p_val}")

    if p_val > 0.5:
        comment = "Хорошо — биты равномерно распределены"
    elif p_val > 0.05:
        comment = "Нормально — небольшие отклонения допустимы"
    else:
        comment = "Плохо — биты распределены неравномерно"
    print(f"Комментарий: {comment}")


if __name__ == "__main__":
    filename = "sources/encrypted.bin"
    bits = read_bin_file_bits(filename)

    autocorrelation_test(bits)
    poker_test(bits, m=4)
    chi_square_test(bits)
