#include "mixcolumns.h"

static uint8_t gmul(uint8_t a, uint8_t b) {
    uint8_t p = 0;
    uint8_t hi_bit_set;
    for (int i = 0; i < 8; i++) {
        if (b & 1) {
            p ^= a;
        }
        hi_bit_set = a & 0x80;
        a <<= 1;
        if (hi_bit_set) {
            a ^= 0x1b; // Полином x^8 + x^4 + x^3 + x + 1
        }
        b >>= 1;
    }
    return p;
}

void mix_columns(uint8_t state[4][4]) {
    uint8_t temp[4];
    for (int c = 0; c < 4; c++) {
        temp[0] = gmul(0x02, state[0][c]) ^ gmul(0x03, state[1][c]) ^ state[2][c] ^ state[3][c];
        temp[1] = state[0][c] ^ gmul(0x02, state[1][c]) ^ gmul(0x03, state[2][c]) ^ state[3][c];
        temp[2] = state[0][c] ^ state[1][c] ^ gmul(0x02, state[2][c]) ^ gmul(0x03, state[3][c]);
        temp[3] = gmul(0x03, state[0][c]) ^ state[1][c] ^ state[2][c] ^ gmul(0x02, state[3][c]);

        state[0][c] = temp[0];
        state[1][c] = temp[1];
        state[2][c] = temp[2];
        state[3][c] = temp[3];
    }
}

void inv_mix_columns(uint8_t state[4][4]) {
    uint8_t temp[4];
    for (int c = 0; c < 4; c++) {
        temp[0] = gmul(0x0e, state[0][c]) ^ gmul(0x0b, state[1][c]) ^ gmul(0x0d, state[2][c]) ^ gmul(0x09, state[3][c]);
        temp[1] = gmul(0x09, state[0][c]) ^ gmul(0x0e, state[1][c]) ^ gmul(0x0b, state[2][c]) ^ gmul(0x0d, state[3][c]);
        temp[2] = gmul(0x0d, state[0][c]) ^ gmul(0x09, state[1][c]) ^ gmul(0x0e, state[2][c]) ^ gmul(0x0b, state[3][c]);
        temp[3] = gmul(0x0b, state[0][c]) ^ gmul(0x0d, state[1][c]) ^ gmul(0x09, state[2][c]) ^ gmul(0x0e, state[3][c]);

        state[0][c] = temp[0];
        state[1][c] = temp[1];
        state[2][c] = temp[2];
        state[3][c] = temp[3];
    }
}

// -----------------------------------------------------------------------------------------

#include <wmmintrin.h>
#include <emmintrin.h> 
#include <smmintrin.h> 
#include <immintrin.h>

static inline __m128i gmul_column(__m128i col, uint8_t factor) {
    __m128i f = _mm_set1_epi8(factor);
    return _mm_gf2p8mul_epi8(col, f);
}

void mix_columns_simd(uint8_t state[4][4]) {
    for (int c = 0; c < 4; c++) {
        __m128i col = _mm_set_epi8(
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            state[3][c], state[2][c], state[1][c], state[0][c]
        );

        __m128i m2 = gmul_column(col, 0x02);
        __m128i m3 = gmul_column(col, 0x03);

        uint8_t temp[4];
        temp[0] = _mm_extract_epi8(m2, 0) ^ _mm_extract_epi8(m3, 1) ^ state[2][c] ^ state[3][c];
        temp[1] = state[0][c] ^ _mm_extract_epi8(m2, 1) ^ _mm_extract_epi8(m3, 2) ^ state[3][c];
        temp[2] = state[0][c] ^ state[1][c] ^ _mm_extract_epi8(m2, 2) ^ _mm_extract_epi8(m3, 3);
        temp[3] = _mm_extract_epi8(m3, 0) ^ state[1][c] ^ state[2][c] ^ _mm_extract_epi8(m2, 3);

        state[0][c] = temp[0];
        state[1][c] = temp[1];
        state[2][c] = temp[2];
        state[3][c] = temp[3];
    }
}

void inv_mix_columns_simd(uint8_t state[4][4]) {
    for (int c = 0; c < 4; c++) {
        __m128i col = _mm_set_epi8(
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            state[3][c], state[2][c], state[1][c], state[0][c]
        );

        __m128i m9  = gmul_column(col, 0x09);
        __m128i m11 = gmul_column(col, 0x0b);
        __m128i m13 = gmul_column(col, 0x0d);
        __m128i m14 = gmul_column(col, 0x0e);

        uint8_t temp[4];
        temp[0] = _mm_extract_epi8(m14, 0) ^ _mm_extract_epi8(m11, 1) ^ _mm_extract_epi8(m13, 2) ^ _mm_extract_epi8(m9, 3);
        temp[1] = _mm_extract_epi8(m9, 0) ^ _mm_extract_epi8(m14, 1) ^ _mm_extract_epi8(m11, 2) ^ _mm_extract_epi8(m13, 3);
        temp[2] = _mm_extract_epi8(m13, 0) ^ _mm_extract_epi8(m9, 1) ^ _mm_extract_epi8(m14, 2) ^ _mm_extract_epi8(m11, 3);
        temp[3] = _mm_extract_epi8(m11, 0) ^ _mm_extract_epi8(m13, 1) ^ _mm_extract_epi8(m9, 2) ^ _mm_extract_epi8(m14, 3);

        state[0][c] = temp[0];
        state[1][c] = temp[1];
        state[2][c] = temp[2];
        state[3][c] = temp[3];
    }
}