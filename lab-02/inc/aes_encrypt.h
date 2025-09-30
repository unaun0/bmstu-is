#ifndef AES_ENCRYPT_H
#define AES_ENCRYPT_H

#include <stdint.h>
#include <string.h>

void aes_ecb_encrypt(const uint8_t* input, uint8_t* output, size_t length, const uint8_t* key);
void aes_ecb_encrypt_upd(const uint8_t* input, uint8_t* output, size_t length, const uint8_t* key);

#endif // AES_ENCRYPT_H
