#include "add_round_key.h"

void add_round_key(uint8_t state[4][4], uint8_t roundKey[4][4]) {
    for (int r = 0; r < 4; r++) {
        for (int c = 0; c < 4; c++) {
            state[r][c] ^= roundKey[r][c];
        }
    }
}

// -----------------------------------------------------------------------------------------

#include <immintrin.h>

void add_round_key_simd(uint8_t state[4][4], uint8_t roundKey[4][4]) {
    __m128i* state_vec = (__m128i*)state;
    __m128i* round_key_vec = (__m128i*)roundKey;

    *state_vec = _mm_xor_si128(*state_vec, *round_key_vec);
}