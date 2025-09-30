#ifndef ADD_ROUND_KEY_H
#define ADD_ROUND_KEY_H

#include <stdint.h>

void add_round_key(uint8_t state[4][4], uint8_t roundKey[4][4]);
void add_round_key_simd(uint8_t state[4][4], uint8_t roundKey[4][4]);

#endif // ADD_ROUND_KEY_H
