#include "shiftrows.h"
#include <stdint.h>


static void rotate_left(uint8_t* row, int n) {
    uint8_t temp;
    for (int i = 0; i < n; i++) {
        temp = row[0];
        for (int j = 0; j < 3; j++) {
            row[j] = row[j + 1];
        }
        row[3] = temp;
    }
}

static void rotate_right(uint8_t* row, int n) {
    uint8_t temp;
    for (int i = 0; i < n; i++) {
        temp = row[3];
        for (int j = 3; j > 0; j--) {
            row[j] = row[j - 1];
        }
        row[0] = temp;
    }
}

void shift_rows(uint8_t state[4][4]) {
    for (int i = 1; i < 4; i++) {
        rotate_left(state[i], i);
    }
}

void inv_shift_rows(uint8_t state[4][4]) {
    for (int i = 1; i < 4; i++) {
        rotate_right(state[i], i);
    }
}

// -----------------------------------------------------------------------------------------

#include <immintrin.h>
#include <stdint.h>

void shift_rows_simd(uint8_t state[4][4]) {
    __m128i s = _mm_loadu_si128((__m128i *)state);

    const __m128i shuffle_mask = _mm_set_epi8(
        14, 13, 12, 15, // row 3
        9, 8, 11, 10,   // row 2
        4, 7, 6, 5,     // row 1
        3, 2, 1, 0      // row 0
    );

    s = _mm_shuffle_epi8(s, shuffle_mask);

    _mm_storeu_si128((__m128i *)state, s);
}

void inv_shift_rows_simd(uint8_t state[4][4]) {
    __m128i s = _mm_loadu_si128((__m128i *)state);

    const __m128i shuffle_mask = _mm_set_epi8(
        12, 15, 14, 13, // row 3
        9, 8, 11, 10,   // row 2
        6, 5, 4, 7,     // row 1
        3, 2, 1, 0      // row 0
    );

    s = _mm_shuffle_epi8(s, shuffle_mask);

    _mm_storeu_si128((__m128i *)state, s);
}
