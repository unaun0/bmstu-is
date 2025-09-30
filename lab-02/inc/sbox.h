#ifndef SBOX_H
#define SBOX_H

#include <stdint.h>

uint8_t sbox_get(uint8_t input);
uint8_t inv_sbox_get(uint8_t input);

void sbox_sub_bytes_simd(uint8_t* state);
void inv_sbox_sub_bytes_simd(uint8_t* state);

extern const uint8_t S_BOX[256];
extern const uint8_t INV_S_BOX[256];

#endif // SBOX_H
