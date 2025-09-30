#ifndef SHIFTROWS_H
#define SHIFTROWS_H

#include <stdint.h>

void shift_rows(uint8_t state[4][4]);
void inv_shift_rows(uint8_t state[4][4]);

void shift_rows_simd(uint8_t state[4][4]);
void inv_shift_rows_simd(uint8_t state[4][4]);

#endif // SHIFTROWS_H
