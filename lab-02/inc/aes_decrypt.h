#ifndef AES_DECRYPT_H
#define AES_DECRYPT_H

#include <stdint.h>
#include <string.h>

void aes_ecb_decrypt(const uint8_t* input, uint8_t* output, size_t length, const uint8_t* key);
void aes_ecb_decrypt_upd(const uint8_t* input, uint8_t* output, size_t length, const uint8_t* key);

#endif // AES_DECRYPT_H
