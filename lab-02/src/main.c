#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>

#include "aes_encrypt.h"
#include "aes_decrypt.h"
#include "key_expansion.h"

static uint8_t* read_file(const char* filename, size_t* length) {
    FILE* file = fopen(filename, "rb");
    if (!file) {
        perror("Ошибка открытия файла");
        return NULL;
    }

    fseek(file, 0, SEEK_END);
    *length = ftell(file);
    fseek(file, 0, SEEK_SET);

    uint8_t* buffer = (uint8_t*)malloc(*length);
    if (!buffer) {
        fclose(file);
        return NULL;
    }

    fread(buffer, 1, *length, file);
    fclose(file);

    return buffer;
}

static int write_file(const char* filename, const uint8_t* data, size_t length) {
    FILE* file = fopen(filename, "wb");
    if (!file) {
        perror("Ошибка записи файла");
        return -1;
    }

    fwrite(data, 1, length, file);
    fclose(file);
    return 0;
}

static double get_elapsed_time(struct timeval start, struct timeval end) {
    return (end.tv_sec - start.tv_sec) +
           (end.tv_usec - start.tv_usec) / 1e6;
}

static void process_aes(const char* input_filename,
                        const char* encrypted_filename,
                        const char* decrypted_filename,
                        const char* key_filename,
                        int use_optimized) {
    size_t length = 0;
    uint8_t* input_data = read_file(input_filename, &length);
    if (!input_data) return;

    uint8_t key[AES_KEY_SIZE];
    generate_key(key);
    if (write_file(key_filename, key, AES_KEY_SIZE) != 0) {
        free(input_data);
        return;
    }
    printf("Ключ сгенерирован и сохранён в %s\n", key_filename);

    size_t padded_length = ((length + 15) / 16) * 16;
    uint8_t* encrypted_data = (uint8_t*)malloc(padded_length);
    uint8_t* decrypted_data = (uint8_t*)malloc(padded_length);
    if (!encrypted_data || !decrypted_data) {
        free(input_data);
        return;
    }

    struct timeval start, end;

    // Шифрование
    gettimeofday(&start, NULL);
    if (use_optimized)
        aes_ecb_encrypt_upd(input_data, encrypted_data, length, key);
    else
        aes_ecb_encrypt(input_data, encrypted_data, length, key);
    gettimeofday(&end, NULL);

    printf("Время шифрования: %.6f секунд\n", get_elapsed_time(start, end));
    write_file(encrypted_filename, encrypted_data, padded_length);
    printf("Файл зашифрован: %s\n", encrypted_filename);
    
    free(input_data);

    // Дешифрование
    size_t enc_length;
    uint8_t* enc_file_data = read_file(encrypted_filename, &enc_length);
    if (!enc_file_data) {
        free(encrypted_data);
        free(decrypted_data);
        return;
    }

    size_t key_len;
    uint8_t* file_key = read_file(key_filename, &key_len);
    if (!file_key || key_len != AES_KEY_SIZE) {
        perror("Ошибка чтения ключа");
        free(enc_file_data);
        free(encrypted_data);
        free(decrypted_data);
        return;
    }

    gettimeofday(&start, NULL);
    if (use_optimized)
        aes_ecb_decrypt_upd(enc_file_data, decrypted_data, enc_length, file_key);
    else
        aes_ecb_decrypt(enc_file_data, decrypted_data, enc_length, file_key);
    gettimeofday(&end, NULL);

    printf("Время дешифрования: %.6f секунд\n", get_elapsed_time(start, end));
    write_file(decrypted_filename, decrypted_data, length);
    printf("Файл расшифрован: %s\n", decrypted_filename);

    free(enc_file_data);
    free(encrypted_data);
    free(decrypted_data);
    free(file_key);
}

int main() {
    const char* input_filename = "sources/input.txt";
    const char* encrypted_filename = "sources/encrypted.bin";
    const char* decrypted_filename = "sources/decrypted.txt";
    const char* key_filename = "sources/key.bin";

    printf("Выберите режим работы:\n");
    printf("1 — Обычная версия AES\n");
    printf("2 — Оптимизированная версия AES\n");
    printf("Введите номер: ");

    int choice = 0;
    if (scanf("%d", &choice) != 1 || (choice != 1 && choice != 2)) {
        printf("Неверный ввод.\n");
        return 1;
    }

    int use_optimized = (choice == 2);
    process_aes(input_filename, encrypted_filename, decrypted_filename, key_filename, use_optimized);

    return 0;
}
